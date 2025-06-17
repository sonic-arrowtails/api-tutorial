from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from . import schemas
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = "12a26e3b2ffa1fdd14304ced9e550a2977167f72b165624b99ebd67d37bc4cb2"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.now(datetime.timezone.utc) + timedelta(minutes=30)
    to_encode.update({"exp":expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=[ALGORITHM])

    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithm=[ALGORITHM])
        id : str = payload.get("user_id")
        if id == None: raise credentials_exception
        token_data = schemas.TokenData(id=id)
        
    except JWTError: raise credentials_exception

    return token_data

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                         detail = "Could not validate credentials",
                                         headers= {"WWW-Authenticate": "Bearer"})
    return verify_access_token(token,credentials_exception)
