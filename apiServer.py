# sys libs
import uuid
import os
import sys
from os.path import join, dirname
# funcs libs
from dotenv import load_dotenv
import json
import numpy as np
import pandas as pd
# api libs
from typing import Union
from pydantic import BaseModel, UUID4, BaseSettings
import requests
from fastapi import FastAPI, Form, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException
# class/funcs
from se.genkey import read_key
from se.contants import d, L
from se.searchscheme import PSE
from cosmosMethod import CosmosClass


parent_dir_name = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parent_dir_name)

dotenv_path = join(dirname(__file__), '.env')

load_dotenv(dotenv_path)
ENDPOINT = os.environ.get("ENDPOINT")
KEY = os.environ.get("KEY")
DATABASE_NAME = os.environ.get("DATABASE_NAME")
DOCUMENT_CONTAINER = os.environ.get("DOCUMENT_CONTAINER")
INDEX_CONTAINER = os.environ.get("INDEX_CONTAINER")
AA1_IP = os.environ.get("AA1_IP")
AA2_IP = os.environ.get("AA2_IP")
AA3_IP = os.environ.get("AA3_IP")


class Settings(BaseSettings):
    secret: str


DEFAULT_SETTINGS = Settings(_env_file=".env")
DB = {
    "users": {}
}
TOKEN_URL = "/login"

app = FastAPI()
manager = LoginManager(DEFAULT_SETTINGS.secret, TOKEN_URL)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@manager.user_loader()
def get_user(email: str):
    return DB["users"].get(email)


def initadd(db_user):
    DB["users"][db_user['email']] = db_user


initadd({'email': 'alice', 'password': 'alice', 'id': uuid.uuid4()})
initadd({'email': 'lily', 'password': 'lily', 'id': uuid.uuid4()})
initadd({'email': 'luke', 'password': 'luke', 'id': uuid.uuid4()})
initadd({'email': 'bob', 'password': 'bob', 'id': uuid.uuid4()})
initadd({'email': 'john', 'password': 'john', 'id': uuid.uuid4()})
initadd({'email': 'mike', 'password': 'mike', 'id': uuid.uuid4()})
initadd({'email': 'khanh', 'password': 'khanh', 'id': uuid.uuid4()})
initadd({'email': 'trung', 'password': 'trung', 'id': uuid.uuid4()})


def verifyattr(uname: str, attribute: str):
    data = json.loads(attribute)
    result = [None, None, None]
    for i in data:
        if i == 'PROVIDER':
            response_AA1 = requests.post(AA1_IP, json={'uname': uname, 'attribute': data[i]})
            result[0] = response_AA1.text
            if (not response_AA1.text):
                return False
        if i == 'PUBLICADMIN':
            response_AA2 = requests.post(AA2_IP, json={'uname': uname, 'attribute': data[i]})
            result[1] = response_AA2.text
            if (not response_AA2.text):
                return False
        if i == 'TRANSACTIONSUPPORT':
            response_AA3 = requests.post(AA3_IP, json={'uname': uname, 'attribute': data[i]})
            if (not response_AA3.text):
                return False
            result[2] = response_AA3.text
    if (not result[0]) and (not result[1]) and (not result[2]):
        return False
    return True


class Data(BaseModel):
    user: dict


class UserCreate(BaseModel):
    username: str
    password: str


class User(UserCreate):
    id: UUID4


@app.post(TOKEN_URL)
def login(attribute=Form(), data: OAuth2PasswordRequestForm = Depends()):
    email = data.username
    password = data.password
    user = get_user(email)
    # verify = verifyattr(email, attribute)
    if not user:
        raise InvalidCredentialsException  # you can also use your own HTTPException
    elif password != user['password']:
        raise InvalidCredentialsException
    # elif not verify:
    #     raise InvalidCredentialsException
    access_token = manager.create_access_token(
        data=dict(sub=email)
    )
    return {'access_token': access_token, 'token_type': 'bearer'}


@ app.get("/")
def root():
    return {"Helllo": "Hello World!"}


@ app.get("/key")
async def get_key(id, user=Depends(manager)):
    try:
        (sk, dummies, primes, kf) = read_key(id)
        return {'key-id': "key-{}".format(id), 'key': {'sk': {'S': json.dumps(sk[2]), 'M1': json.dumps(sk[0]), 'M2': json.dumps(sk[1])}, 'dummies': json.dumps(dummies), 'primes': json.dumps(primes), 'kf': str(kf, encoding='latin1')}}
    except:
        raise HTTPException(status_code=404, detail="NOT FOUND")


@ app.get("/document")
async def get_document(id, user=Depends(manager)):
    try:
        cosmos = CosmosClass(ENDPOINT, KEY, DATABASE_NAME)
        cosmos.set_container(DOCUMENT_CONTAINER)
        document = cosmos.query_document_by_id(id)
    except:
        raise HTTPException(status_code=500, detail="INTERNAL SERVER ERROR")
    if len(document) > 0:
        return document[0]
    else:
        raise HTTPException(status_code=404, detail="NOT FOUND")


class SearchItem(BaseModel):
    key: str
    trapdoor: str
    basic: Union[bool, None] = True
    andQ: Union[bool, None] = True


@ app.post("/search")
async def search_calculation(search_item: SearchItem, user=Depends(manager)):
    print("[LOG]: Execute Search")
    try:
        print(search_item.key)
        se = PSE(d, L)
        se.set_detail(search_item.basic, search_item.andQ)
        trapdoor_decode = np.asarray(json.loads(search_item.trapdoor))
        se.set_trapdoor(trapdoor_decode)
        cosmos_instance = CosmosClass(ENDPOINT, KEY, DATABASE_NAME)
        cosmos_instance.set_container(INDEX_CONTAINER)
        container = cosmos_instance.get_container()
        list_read = list(container.read_all_items(max_item_count=10))
        for x in list_read:
            index = pd.read_json(x['data'])
            se.set_index(index)
            se.set_search()
        result = se.get_result()
        if len(result) == 0:
            return HTTPException(status_code=404, detail="NOT FOUND")
        return {'document_match': result}
    except:
        raise HTTPException(status_code=500, detail="INTERNAL SERVER ERROR")
