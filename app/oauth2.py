from datetime import datetime, timedelta
import jwt

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "655d041f3ef4b80d43bd74e14cc47c17b459ac0d88787cbd85625dbe8583186b"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    # generating the expiration time of the token
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt

