from fastapi import HTTPException
import mysql.connector
import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from src.database import dbconfig
from src.token import tokenconfig
import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from typing import Annotated, List, Union


SECRET_KEY = tokenconfig["SECRET_KEY"]
ALGORITHM = tokenconfig["ALGORITHM"]
ACCESS_TOKEN_EXPIRE_DAYS = tokenconfig["ACCESS_TOKEN_EXPIRE_DAYS"]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserModel:
# 驗證密碼
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    # 加密密碼
    def get_password_hash(password):
        return pwd_context.hash(password)

    # 取得使用者by email
    def get_user(email):
        try:
            cnxpool = mysql.connector.pooling.MySQLConnectionPool(**dbconfig)
            cnx = cnxpool.get_connection()
            cursor = cnx.cursor()

            sql_string = "SELECT * FROM member WHERE email = %s"
            cursor.execute(sql_string, (email,))
            data = cursor.fetchone()
            
            if not data:
                return None

            return data

        except Exception as e:
            raise HTTPException(status_code=500, detail="伺服器內部錯誤")
        
        finally:
            if cursor:
                cursor.close()
            if cnx:
                cnx.close()
        
    # 確認是否有使用者
    def authenticate_user(email, password):
        user = UserModel.get_user(email)
        if not user:
            return False
        if not UserModel.verify_password(password, user[3]):
            return False
        return user

    # 產生TOKEN
    def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    # 使用TOKEN取得使用者
    async def get_current_user(token):
        try:
            # 確認TOKEN
            cnxpool = mysql.connector.pooling.MySQLConnectionPool(**dbconfig)
            cnx = cnxpool.get_connection()
            cursor = cnx.cursor()

            sql_string = "SELECT * FROM member WHERE token = %s"
            cursor.execute(sql_string, (token,))
            data = cursor.fetchone()
            
            # 確認是否有TOKEN
            if not data:
                return None
            
            # 解碼TOKEN
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email = payload.get("sub")
            if email is None:
                return None
            return email

        except Exception as e:
            raise HTTPException(status_code=500, detail="伺服器內部錯誤")

        finally:
            if cursor:
                cursor.close()
            if cnx:
                cnx.close()

    def create_user(name, email, password):
        try:
            cnxpool = mysql.connector.pooling.MySQLConnectionPool(**dbconfig)
            cnx = cnxpool.get_connection()
            cursor = cnx.cursor()

            sql_string = "INSERT INTO member (name, email, password) VALUES (%s, %s, %s)"
            cursor.execute(sql_string, (name, email, password))
            cnx.commit()

            return True

        except Exception as e:
            raise HTTPException(status_code=500, detail="伺服器內部錯誤")

        finally:
            if cursor:
                cursor.close()
            if cnx:
                cnx.close()

    def update_token(email, token):
        try:
            cnxpool = mysql.connector.pooling.MySQLConnectionPool(**dbconfig)
            cnx = cnxpool.get_connection()
            cursor = cnx.cursor()

            sql_string = "UPDATE member SET token = %s WHERE email = %s"
            cursor.execute(sql_string, (token, email))
            cnx.commit()

            return True

        except Exception as e:
            raise HTTPException(status_code=500, detail="伺服器內部錯誤")

        finally:
            if cursor:
                cursor.close()
            if cnx:
                cnx.close()