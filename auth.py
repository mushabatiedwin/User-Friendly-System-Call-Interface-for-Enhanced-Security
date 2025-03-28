import datetime
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError  # Correct import

# Authentication Setup
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Fake User Database
fake_users_db = {
    "admin": {"username": "admin", "password": "admin123"},
    "Edwin": {"username": "Edwin", "password": "Mushabati"}
}

# Function to Create JWT Token
def create_jwt_token(username: str):
    expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    return jwt.encode({"sub": username, "exp": expiration}, SECRET_KEY, algorithm=ALGORITHM)

# Function to Validate and Decode JWT Token
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if not username or username not in fake_users_db:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return {"username": username}
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except JWTError:  # Fix the incorrect DecodeError
        raise HTTPException(status_code=401, detail="Invalid token")
