from fastapi import FastAPI, HTTPException
from se.genkey import read_key
import json

app = FastAPI()


@app.get("/")
def root():
  return {"Helllo": "Hello World!"}


@app.get("/key/")
async def get_key(key_id):
  try:
    (sk, dummies, primes, kf) = read_key(key_id)
    return {'key-id': "key-{}".format(key_id), 'key': {'sk': {'S': json.dumps(sk[2]), 'M1': json.dumps(sk[0]), 'M2': json.dumps(sk[1])}, 'dummies': json.dumps(dummies), 'primes': json.dumps(primes), 'kf': str(kf, encoding='latin1')}}
  except:
    raise HTTPException(status_code=404, detail="Item not found")
