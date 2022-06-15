from urllib import response
import requests
import numpy as np
import json
# class/funcs
from se.searchscheme import PSE
from se.contants import d, L
from se.genkey import read_key
from se.utils import NumpyArrayEncoder


def generate_trapdoor(keywords, key):
    se = PSE(d, L)
    se.set_key(key_path="./storage/256/key/key256-01.json")
    basic = False
    andQ = False
    se.set_detail(basic, andQ)
    se.insert_query(keywords)
    trapdoor = se.get_trapdoor()
    data = {'trapdoor': json.dumps(trapdoor, cls=NumpyArrayEncoder),
            'key': key, 'basic': basic, 'andQ': andQ}
    response = requests.post("http://127.0.0.1:3000/search", json=data)
    return response


async def read_document(doc_id):
    response = await requests.get("http://127.0.0.1:3000/document", params={'id': doc_id})
    file = json.loads(response.text)
    with open('document.json', 'w') as f:
        json.dump(file, f)
    f.close()

if __name__ == "__main__":
    keyword = ["vietcombank"]
    a = generate_trapdoor(keyword, "key256-01")
    print(a.text)
    read_document("document23")
