from fastapi import HTTPException
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import FastAPI

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
app = FastAPI()


from datetime import datetime, timedelta
from typing import Union
from fastapi import FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError,jwt
from passlib.context import CryptContext
from database.models.users import TokenData,User
from pydantic import BaseModel

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_user(db, email: str):
    for index,data in enumerate(db):
        if email == db[index]['email']:
            return data
    return None
        
def verify_password(plain_password, password):
    verify = pwd_context.verify(plain_password, password)
    return verify

async def authenticate_user(data_db, email: str, password: str):
    user = get_user(data_db, email)
    if not user:
        return False
    if not verify_password(password, user['password']):
        return False
    return user
