# libs
import json
import requests
# class/funcs
from abe.abenc_dacmacs_yj14 import DACMACS
from charm.core.engine.util import bytesToObject
from charm.toolbox.pairinggroup import extract_key
from charm.toolbox.symcrypto import SymmetricCryptoAbstraction


class DecryptDocument:
    def __init__(self, groupObj):
        self.groupObj = groupObj
        self.dac = DACMACS(self.groupObj)

    def _get_object_frombyte(self, x):
        return bytesToObject(x.encode('UTF-8'), self.groupObj)

    def set_GPP(self, url):
        x = requests.get(url)
        self.GPP = self._get_object_frombyte(x.text)

    def decrypt(self, data: dict, attributekey: dict):
        if (isinstance(data, str)):
            return data
        k = self._get_object_frombyte(data['key'])
        TK = self.dac.generateTK(self.GPP, k, attributekey['authoritySecretKeys'], attributekey['keys'][0])
        key = self.dac.decrypt(k, TK, attributekey['keys'][1])
        res = data.copy()
        del res['key']
        if (key == False):
            res = dict.fromkeys(res, "*** NO PERMISSION ***")
            return res
        a = SymmetricCryptoAbstraction(extract_key(key))
        for i in res:
            ob = self._get_object_frombyte(res[i])
            s = a.decrypt(ob)
            try:
                s = bytesToObject(s, self.groupObj)
            except:
                s = s.decode('UTF-8')
            res[i] = s
        return res

    def get_result(self, data, attributekey):
        ab = data['Provider']
        for k in ab:
            if (k == 'Management and construction information'):
                for j in ab[k]:
                    data['Provider'][k][j] = self.decrypt(data['Provider'][k][j], attributekey)
                continue
            data['Provider'][k] = self.decrypt(data['Provider'][k], attributekey)
        for k in data:
            if (k == 'Provider') or (k == 'id'):
                continue
            for j in data[k]:
                data[k][j] = self.decrypt(data[k][j], attributekey)
        return json.dumps(data, indent=10)
