from io import BytesIO
import pickle
from typing import Union
from pydantic import BaseModel
import requests
import json
import sys
import os
from os.path import join, dirname
from dotenv import load_dotenv
from fastapi import FastAPI, Form, HTTPException, UploadFile, File
from fastapi.staticfiles import StaticFiles
from requests import request
# class/funcs
from se.searchscheme import PSE
from se.contants import d, L
from se.genkey import read_key
from se.utils import NumpyArrayEncoder
from abe.utils import loadObject, remove_unuse_key, groupObj, bytesToObject
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
    # key: str
    basicScheme: Union[bool, None] = True
    andQuery: Union[bool, None] = True


class User(BaseModel):
    username: str
    password: str


@app.post("/login")
def get_authen(username=Form(), password=Form(), upload_file: UploadFile = File()):
    attr = json.load(upload_file.file)
    response = requests.post(
        url="{}/login".format(BACKEND_IP),
        data={"username": username, "password": password, "attribute": json.dumps(attr)})
    print(response.status_code)
    if (response.status_code == 401 or response.status_code == 500):
        raise HTTPException(status_code=401, detail=response.text)
    token = json.loads(response.text)
    update_token = '{} {}'.format(token["token_type"], token["access_token"])
    setToken(update_token)
    return {"detail": "Login Success", "data": token}


@app.post("/search")
def generate_trapdoor(
        keywords: list = Form(),
        basicScheme: bool = Form(),
        andQuery: bool = Form(),
        key: UploadFile = File()):
    se = PSE(d, L)
    try:
        # se.set_key(key_path="storage/256/key/{}.json".format(body.key))
        se.set_key_file(key.file)
    except:
        raise HTTPException(status_code=500, detail="CANNOT READ KEY")
    basic = basicScheme
    andQ = andQuery
    keywords = keywords[0].split(',')
    se.set_detail(basic, andQ)
    se.insert_query(keywords)
    trapdoor = se.get_trapdoor()
    data = {'trapdoor': json.dumps(trapdoor, cls=NumpyArrayEncoder),'key': 'key256-01','basic': basic, 'andQ': andQ}
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
def decrypt_document(doc: UploadFile = File(), user_path: UploadFile = File()):
    ddc = DecryptDocument(groupObj)
    document = json.load(doc.file)
    document_id = document['id']
    temp = pickle.load(user_path.file)
    user_key = bytesToObject(temp, groupObj)
    ddc.set_GPP(GPP_IP)
    plaint_text = ddc.get_result(document, user_key)
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
