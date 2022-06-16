# libs
import os
import sys
from fastapi import FastAPI, HTTPException
from typing import Union
import json
from dotenv import load_dotenv
from os.path import join, dirname
from pydantic import BaseModel
import numpy as np
import pandas as pd
from requests import request
# class/funcs
from se.genkey import read_key
from se.contants import d, L
from se.searchscheme import PSE
from cosmosMethod import CosmosClass

app = FastAPI()

parent_dir_name = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(parent_dir_name)

dotenv_path = join(dirname(__file__), '.env')

load_dotenv(dotenv_path)
ENDPOINT = os.environ.get("ENDPOINT")
KEY = os.environ.get("KEY")
DATABASE_NAME = os.environ.get("DATABASE_NAME")
DOCUMENT_CONTAINER = os.environ.get("DOCUMENT_CONTAINER")
INDEX_CONTAINER = os.environ.get("INDEX_CONTAINER")


class SearchItem(BaseModel):
    key: str
    trapdoor: str
    basic: Union[bool, None] = True
    andQ: Union[bool, None] = True


class UserAuthentication(BaseModel):
    username: str
    password: str
    attribute: list


@ app.post("/authentication")
def authentication_user(user: UserAuthentication):

    verify = request.post()

    return


@ app.get("/")
def root():
    return {"Helllo": "Hello World!"}


@ app.get("/key")
async def get_key(id):
    try:
        (sk, dummies, primes, kf) = read_key(id)
        return {'key-id': "key-{}".format(id), 'key': {'sk': {'S': json.dumps(sk[2]), 'M1': json.dumps(sk[0]), 'M2': json.dumps(sk[1])}, 'dummies': json.dumps(dummies), 'primes': json.dumps(primes), 'kf': str(kf, encoding='latin1')}}
    except:
        raise HTTPException(status_code=404, detail="NOT FOUND")


@ app.get("/document")
async def get_document(id):
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


@ app.post("/search")
async def search_calculation(search_item: SearchItem):
    try:
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
        print(result)
        if len(result) == 0:
            return HTTPException(status_code=404, detail="NOT FOUND")
        return {'document_match': result}
    except:
        raise HTTPException(status_code=500, detail="INTERNAL SERVER ERROR")
