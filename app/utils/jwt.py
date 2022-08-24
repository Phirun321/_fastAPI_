import time
from typing import Dict

import jwt



JWT_SECRET = "secret"
JWT_ALGORITHM = "HS256"

def token_response(token: str):
    return {
        "access_token": token
    }

def signJWT(user: str) -> Dict[str, str]:
    payload = {
        "user": user,
        "expires": time.time()+10800
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM )

    return token_response(token)
    
def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=JWT_ALGORITHM)
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}