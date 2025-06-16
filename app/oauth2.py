from jose import JWTError, jwt
from datetime import datetime, timedelta

SECRET_KEY = "12a26e3b2ffa1fdd14304ced9e550a2977167f72b165624b99ebd67d37bc4cb2"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=30)
    to_encode.update({"exp":expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt
