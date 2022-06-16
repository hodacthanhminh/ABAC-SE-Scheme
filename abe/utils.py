# libs
import json
import pickle
from charm.core.engine.util import bytesToObject
from charm.toolbox.pairinggroup import PairingGroup

groupObj = PairingGroup('SS512')


def getvalueptfile(filename):
    path = filename
    file = open(path, "r")
    data = json.load(file)
    file.close()
    return data


def loadObject(filename):
    file = open(filename, "rb")
    x = pickle.load(file)
    y = bytesToObject(x, groupObj)
    file.close()
    return y


def remove_unuse_key(doc: dict):
    del doc["_rid"]
    del doc['_self']
    del doc['_etag']
    del doc['_attachments']
    del doc['_ts']
    return doc
