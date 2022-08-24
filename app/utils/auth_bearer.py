
from fastapi import Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from fastapi import HTTPException
from jose import JWTError,jwt
from database.models.users import TokenData
from .functions import get_user
from .jwt import decodeJWT
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
security = HTTPBearer()

def access_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    return token if token else False
    
async def current_user(token: str = Depends(access_token)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decodeJWT(token)
        if payload is None:
            raise credentials_exception
        token_data = payload['user']
    except JWTError:
        raise credentials_exception
    return token_data

async def verify_isAdmin(user:dict = Depends(current_user)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="You're not admin",
        headers={"WWW-Authenticate": "Bearer"},
    )
    role = user['role']
    if role != "admin":
        raise credentials_exception
    else:
        return True
        
async def verify_isAdmin(user:dict = Depends(current_user)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="You're not super user",
        headers={"WWW-Authenticate": "Bearer"},
    )
    role = user['role']
    if role != "super_user":
        raise credentials_exception
    else:
        return True
        
async def verify_isAdmin(user:dict = Depends(current_user)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="You're not normal user",
        headers={"WWW-Authenticate": "Bearer"},
    )
    role = user['role']
    if role != "user":
        raise credentials_exception
    else:
        return True

# it will take for future in case user have attribute status(active or inactive)
# async def get_current_active_user(current_user: User = Depends(get_current_user)):
#     if current_user.disabled:
#         raise HTTPException(status_code=400, detail="Inactive user")
#     return current_user