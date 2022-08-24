from urllib import request
from fastapi import FastAPI

from routers import items, users, admin

app = FastAPI()
# import uvicorn

# if __name__ == "__main__":
#     uvicorn.run("server.app:app", host="0.0.0.0", port=8000, reload=True)

from datetime import datetime, timedelta
from typing import Union
import os
import time
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

# # to get a string like this run:
# # openssl rand -hex 32
# SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30
# # print(os.environ["SECRET_KEY"],"env file::::::::")

# fake_users_db = {
#     "user1": {
#         "username": "johndoe",
#         "full_name": "John Doe",
#         "email": "johndoe@example.com",
#         "hashed_password": "$2b$12$wlqf9sx7JxEVuc9FbtAno.7bbEKtU.x/e2aWknMbTwGDzv0HmF3uW",
#         "disabled": False,
#     },
#     "user2": {
#         "username": "phirun",
#         "full_name": "John Doe",
#         "email": "phirun@example.com",
#         "hashed_password": "$2b$12$wlqf9sx7JxEVuc9FbtAno.7bbEKtU.x/e2aWknMbTwGDzv0HmF3uW",
#         "disabled": False,
#     }
# }


# class Token(BaseModel):
#     access_token: str
#     token_type: str


# class TokenData(BaseModel):
#     username: Union[str, None] = None


# class User(BaseModel):
#     username: str
#     email: Union[str, None] = None
#     full_name: Union[str, None] = None
#     disabled: Union[bool, None] = None


# class UserInDB(User):
#     hashed_password: str


# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# # print('auth:::::::::::::', tokenUrl)
# app = FastAPI()


# def verify_password(plain_password, hashed_password):
#     # print('plain_pa, hashed_pa', plain_password, hashed_password)
#     a = pwd_context.verify(plain_password, hashed_password)
#     print('a::::::::', a)
#     return pwd_context.verify(plain_password, hashed_password)


# def get_password_hash(password):
#     return pwd_context.hash(password)

# b = get_password_hash("12345")
# # print('hase password::::', b)
# def get_user(db, username: str):
#     print('db:::::::::', db)
#     if "user2" in db:
#         user_dict = db["user1"]
#         # print('user dict :::::::::', user_dict)
#         return UserInDB(**user_dict)


# def authenticate_user(fake_db, username: str, password: str):
#     print('fake db:::::::::', fake_db)
#     user = get_user(fake_db, username)
#     print('username , password', username,password)
#     if not user:
#         return False
#     if not verify_password(password, user.hashed_password):
#         return False
#     return user


# def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt


# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     print('depend on auth::::::', oauth2_scheme, token)
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         username: str = payload.get("sub")
#         if username is None:
#             raise credentials_exception
#         token_data = TokenData(username=username)
#     except JWTError:
#         raise credentials_exception
#     user = get_user(fake_users_db, username=token_data.username)
#     print('user::::::::::::', user)
#     if user is None:
#         raise credentials_exception
#     return user


# async def get_current_active_user(current_user: User = Depends(get_current_user)):
#     print(current_user.disabled,'current user::::::::::;;;;')
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user

# from fastapi import Request
# # @app.middleware("http")
# # async def add_process_time_header(request: Request, call_next):
# #     start_time = time.time()
# #     response = await call_next(request)
# #     process_time = time.time() - start_time
# #     response.headers["X-Process-Time"] = str(process_time)
# #     print('request::::::::::', response)
#     # return response
# @app.post("/token", response_model=Token)
# async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
#     user = authenticate_user(fake_users_db, form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.username}, expires_delta=access_token_expires
#     )
#     return {"access_token": access_token, "token_type": "bearer"}


# @app.get("/users/me/", response_model=User)
# async def read_users_me(current_user: User = Depends(get_current_active_user)):
#     print('current user::::::', current_user)
#     return current_user


# @app.get("/users/me/items/")
# async def read_own_items(current_user: User = Depends(get_current_active_user)):
#     return [{"item_id": "Foo", "owner": current_user.username}]



app.include_router(users.router)
app.include_router(items.router)
app.include_router(admin.router)


@app.get("/")
async def root():
    return {"message": "Hello I'm Phirun !"}

