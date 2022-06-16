import uuid
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseSettings, BaseModel, UUID4
from fastapi.responses import FileResponse
import os

from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException


class Settings(BaseSettings):
    secret: str  # automatically taken from environment variable


class Data(BaseModel):
    user: dict


class UserCreate(BaseModel):
    email: str
    password: str


class User(UserCreate):
    id: UUID4


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


# @app.get("/")
# def index():
initadd({'email': 'alice', 'password': 'alice', 'id': uuid.uuid4()})
initadd({'email': 'lily', 'password': 'lily', 'id': uuid.uuid4()})
initadd({'email': 'luke', 'password': 'luke', 'id': uuid.uuid4()})
initadd({'email': 'bob', 'password': 'bob', 'id': uuid.uuid4()})
initadd({'email': 'john', 'password': 'john', 'id': uuid.uuid4()})
initadd({'email': 'mike', 'password': 'mike', 'id': uuid.uuid4()})


@app.post(TOKEN_URL)
def login(data: OAuth2PasswordRequestForm = Depends()):
    email = data.username
    password = data.password
    user = get_user(email)
    if not user:
        raise InvalidCredentialsException  # you can also use your own HTTPException
    elif password != user['password']:
        raise InvalidCredentialsException
    access_token = manager.create_access_token(
        data=dict(sub=email)
    )
    return {'access_token': access_token, 'token_type': 'bearer'}


class DocData(BaseModel):
    name: str


@app.post("/private")
def private_route(data: DocData, user=Depends(manager)):
    return {"detail": f"Welcome {user['email']}", "name": data.name}
