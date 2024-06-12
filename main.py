from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.exceptions import HTTPException
from jose import JWTError, jwt
from typing import Optional
from description import get_seo
from specifications import get_spec
import urllib.request


app = FastAPI()

SECRET_KEY = "rSDntr5pGzC9q82_WlIdDY3_UhYOvTse6hjKM61vygE"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
import datetime

def create_access_token(data: dict, expires_delta: Optional[datetime.timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@app.post("/token")
async def login_for_access_token():
    access_token = create_access_token(data={})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/get_specifications")
def get_sign(token:str, brand:str, model:str, part_num:str=''):
    try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            # Здесь вы можете выполнить проверку токена и получить информацию о пользователе из токена
    except JWTError:
        raise HTTPException(status_code=401, detail="Неверные учетные данные")

    return get_spec(brand, model, part_num)

@app.get("/get_description")
def AI_description(brand, model, token):
    try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            # Здесь вы можете выполнить проверку токена и получить информацию о пользователе из токена
    except JWTError:
        raise HTTPException(status_code=401, detail="Неверные учетные данные")
    res = get_seo(str(brand)+str(model))
    return res

@app.post("/get_ip")
def ip():
    return urllib.request.urlopen('https://ident.me').read().decode('utf8')
