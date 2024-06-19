from datetime import datetime, timedelta, timezone
from typing import List, Union
from fastapi import APIRouter, Depends,  HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, EmailStr
from database import dbconfig
import mysql.connector
from mysql.connector import pooling
import jwt
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from config import tokenconfig


user = APIRouter()


class SuccessResponse(BaseModel):
    ok: bool = True

class ErrorResponse(BaseModel):
    error: bool = True
    message: str = "請按照情境提供對應的錯誤訊息"

class SignUpUser(BaseModel):
    name: str = "test"
    email: EmailStr = "test@gmail.com"
    password: str = "test"

class SignInUser(BaseModel):
    email: EmailStr = "test@gmail.com"
    password: str = "test"


class SignInResponse(BaseModel):
    token: str = "a21312xzDSA"


class UserAuthInfo(BaseModel):
    id: int = 1
    email: EmailStr ="test@gmail.com"
    password: str = "test"

class SignInAuth(BaseModel):
    data: List[UserAuthInfo]



SECRET_KEY = tokenconfig["SECRET_KEY"]
ALGORITHM = tokenconfig["ALGORITHM"]
ACCESS_TOKEN_EXPIRE_DAYS = tokenconfig["ACCESS_TOKEN_EXPIRE_DAYS"]


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt




@user.post("/user", summary="註冊一個新的會員", responses={
              200: {"model": SuccessResponse, "description": "註冊成功"},
              400: {"model": ErrorResponse,"description": "註冊失敗，重複的 Email 或其他原因"},
              500: {"model": ErrorResponse, "description": "伺服器內部錯誤"}})

async def post_user(user: SignUpUser):

    try: 
        cnxpool = mysql.connector.pooling.MySQLConnectionPool(**dbconfig)
        cnx = cnxpool.get_connection()
        cursor = cnx.cursor()

        sql_string = "SELECT * FROM member WHERE email = %s"
        cursor.execute(sql_string, (user.email,))
        if cursor.fetchone():
            return ErrorResponse(message="此信箱已被註冊")
        
        hashed_password = pwd_context.hash(user.password)
        
        sql_string = "INSERT INTO member (name, email, password) VALUES (%s, %s, %s)"
        val = (user.name, user.email, hashed_password)
        cursor.execute(sql_string, val)
        cnx.commit()
        cursor.close()
        cnx.close()

        return {"ok": True}

    except Exception as e:
        raise HTTPException(status_code=500, detail="伺服器內部錯誤")

    
@user.get("/user/auth", summary="取得當前登入的會員資訊", responses = {
    200: {"model": UserAuthInfo, "description": "已登入的會員資料，null 表示未登入"},
})
async def get_user_auth(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="未登入或token無效")
        
        cnxpool = mysql.connector.pooling.MySQLConnectionPool(**dbconfig)
        cnx = cnxpool.get_connection()
        cursor = cnx.cursor()
        
        sql_string = "SELECT id, name, email FROM member WHERE email = %s"
        cursor.execute(sql_string, (email,))
        data = cursor.fetchone()
        cursor.close()
        cnx.close()

        if data:
            user_info = {"id": data[0], "name": data[1], "email": data[2]}
            return {"data": user_info}
        else:
            return {"data": None}

    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="未登入或 token 無效")
    except Exception as e:
        raise HTTPException(status_code=500, detail="伺服器內部錯誤")



@user.put("/user/auth", summary="登入會員帳戶", responses = {
    200: {"model": SignInResponse, "description": "登入成功，得有效期為七天的 JWT 加密字串"},
    400: {"model": ErrorResponse, "description": "登入失敗，帳號或密碼錯誤或其他原因"},
    500: {"model": ErrorResponse, "description": "伺服器內部錯誤"}
})
async def put_user_auth(user: SignInUser):
    try: 
        cnxpool = mysql.connector.pooling.MySQLConnectionPool(**dbconfig)
        cnx = cnxpool.get_connection()
        cursor = cnx.cursor()

        sql_string = "SELECT * FROM member WHERE email = %s"
        cursor.execute(sql_string, (user.email,))
        data = cursor.fetchone()

        if data and verify_password(user.password, data[3]):

            access_token_expires = timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
            access_token = create_access_token(
                data={"sub": user.email}, expires_delta=access_token_expires
            )
           
            sql_string = "UPDATE member SET token = %s WHERE email = %s"
            val = (access_token, user.email)
            cursor.execute(sql_string, val)
            cnx.commit()
            cursor.close()
            cnx.close()

            return {"token": access_token}
        
        else:
            return ErrorResponse(message="帳號或密碼錯誤")

    except Exception as e:
        raise HTTPException(status_code=500, detail="伺服器內部錯誤")