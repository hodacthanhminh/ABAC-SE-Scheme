# libs
import os
import sys
from fastapi import FastAPI, HTTPException
import json
from dotenv import load_dotenv
from os.path import join, dirname
# class/funcs
from se.genkey import read_key
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


@app.get("/")
def root():
    return {"Helllo": "Hello World!"}


@app.get("/key")
async def get_key(id):
    try:
        (sk, dummies, primes, kf) = read_key(id)
        return {'key-id': "key-{}".format(id), 'key': {'sk': {'S': json.dumps(sk[2]), 'M1': json.dumps(sk[0]), 'M2': json.dumps(sk[1])}, 'dummies': json.dumps(dummies), 'primes': json.dumps(primes), 'kf': str(kf, encoding='latin1')}}
    except:
        raise HTTPException(status_code=404, detail="NOT FOUND")


@app.get("/document")
async def get_document(id):
    try:
        cosmos = CosmosClass(ENDPOINT, KEY, DATABASE_NAME)
        cosmos.set_container(DOCUMENT_CONTAINER)
        document = cosmos.query_document_by_id(id)
    except:
        raise HTTPException(status_code=500, detail="INTERNAL SERVER ERROR")
    if len(document) > 0:
        return document
    else:
        raise HTTPException(status_code=404, detail="NOT FOUND")
