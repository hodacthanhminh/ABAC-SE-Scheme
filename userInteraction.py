from typing import Union
from pydantic import BaseModel
import requests
import json
import sys
import os
from os.path import join, dirname
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from requests import request
# class/funcs
from se.searchscheme import PSE
from se.contants import d, L
from se.genkey import read_key
from se.utils import NumpyArrayEncoder
from abe.utils import loadObject, remove_unuse_key, groupObj
from abe.decryptDocument import DecryptDocument

parent_dir_name = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parent_dir_name)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
GPP_IP = os.environ.get("GPP_IP")
BACKEND_IP = os.environ.get("BACKEND_IP")

app = FastAPI()
app.mount("/storage", StaticFiles(directory="storage"), name="storage")


DB_token = {
    "user_token": "",
    "user_attribute": ""
}

Headers = {
    'Authorization': ""
}


def setToken(token: str):
    DB_token["user_token"] = token
    setHeader()


def setHeader():
    Headers["Authorization"] = DB_token["user_token"]


class SearchBody(BaseModel):
    keywords: list
    key: str
    basicScheme: Union[bool, None] = True
    andQuery: Union[bool, None] = True


class User(BaseModel):
    username: str
    password: str


@app.post("/login")
def get_authen(body: User):
    response = requests.post(
        url="{}/login".format(BACKEND_IP),
        data={"username": body.username, "password": body.password})
    token = json.loads(response.text)
    update_token = '{} {}'.format(token["token_type"], token["access_token"])
    print(update_token)
    setToken(update_token)
    return {"detail": "Login Success", "data": token}


@app.post("/search")
def generate_trapdoor(body: SearchBody):
    se = PSE(d, L)
    try:
        se.set_key(key_path="./storage/256/key/{}.json".format(body.key))
    except:
        raise HTTPException(status_code=500, detail="CANNOT READ KEY")
    basic = body.basicScheme
    andQ = body.andQuery
    se.set_detail(basic, andQ)
    se.insert_query(body.keywords)
    trapdoor = se.get_trapdoor()
    data = {'trapdoor': json.dumps(trapdoor, cls=NumpyArrayEncoder),
            'key': body.key, 'basic': basic, 'andQ': andQ}
    print(data["key"])
    response = requests.post(url="{}/search".format(BACKEND_IP), json=data, headers=Headers)
    return json.loads(response.text)


@app.get("/get_document")
def get_document(doc_id):
    response = requests.get(url="{}/document".format(BACKEND_IP), params={'id': doc_id}, headers=Headers)
    file = json.loads(response.text)
    file = remove_unuse_key(file)
    storage_path = 'storage/searchResult/encrypted/{}.json'.format(doc_id)
    os_path = os.path.join(os.getcwd(), storage_path)
    with open(os_path, 'w') as f:
        json.dump(file, f)
    f.close()
    return {'storage at': storage_path, 'cipher_text': file}


class DecryptRequest(BaseModel):
    document_path: str
    user_path: str


@app.post("/decrypt_docunment")
def decrypt_document(body: DecryptRequest):
    user_attribute = loadObject(body.user_path)
    ddc = DecryptDocument(groupObj)
    os_path = os.path.join(os.getcwd(), body.document_path)
    with open(os_path, "r") as f:
        document = json.load(f)
        document_id = document['id']
        f.close()
    ddc.set_GPP(GPP_IP)
    plaint_text = ddc.get_result(document, user_attribute)
    storage_path = 'storage/searchResult/decrypted/{}.json'.format(document_id)
    os_path = os.path.join(os.getcwd(), storage_path)
    with open(os_path, "w") as f:
        f.write(plaint_text)
    return {'storage at': storage_path, 'plaint_text': plaint_text}

# if __name__ == "__main__":
#     # keyword = ["vietcombank", "agribank"]
#     # match_docs = generate_trapdoor(keyword, "key256-01").text
#     # print(match_docs)
#     # read_document("document25")
#     with open("storage/searchResult/decryptDocuemnt.json", "w") as f:
#         data = decrypt_document("storage/searchResult/{}.json".format("document25"), "Trungkey.txt")
#         f.write(data)
