from datetime import datetime, timedelta, timezone
import json
from typing import Annotated, List, Optional, Union
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials, HTTPBasicCredentials
from pydantic import BaseModel, EmailStr
from database import dbconfig
import mysql.connector
from mysql.connector import pooling
import jwt
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from config import tokenconfig
import requests
import uuid 
from datetime import datetime

SECRET_KEY = tokenconfig["SECRET_KEY"]
ALGORITHM = tokenconfig["ALGORITHM"]
ACCESS_TOKEN_EXPIRE_DAYS = tokenconfig["ACCESS_TOKEN_EXPIRE_DAYS"]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/auth")
http_bearer = HTTPBearer()

class ErrorResponse(BaseModel):
    error: bool = True
    message: str = "請按照情境提供對應的錯誤訊息"

class Attraction(BaseModel):
    id: int = 10
    name: str = "平安鐘"
    address: str = "臺北市大安區忠孝東路 4 段"
    image: str = "https://yourdomain.com/images/attraction/10.jpg"

class Trip(BaseModel):
    attraction: Attraction
    date: str = "2022-01-31"
    time: str = "afternoon"

class Contact(BaseModel):
    name: str = "test"
    email: str = "test@test.com"
    phone: str = "0912345678"

class OrderDetails(BaseModel):
    price: int = 2000
    trip: Trip 
    contact: Contact

class Order(BaseModel):
    prime: str =  "前端從第三方金流 TapPay 取得的交易碼"
    order: OrderDetails


order = APIRouter()


async def get_current_user(token: str):
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
        
        cursor.close()
        cnx.close()
        
        # 解碼TOKEN
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            return None
        return email

    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="沒有授權")

TAPPAY_PARTNER_KEY = "partner_eB22IOhRZsaXl7IBbo8Uss1qd421hd5rVCO7R6MCtT4kpHsj9lDeDdUt"
TAPPAY_API_URL = "https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime"


@order.post("/orders", summary= "建立新的訂單，並完成付款程序", responses={
              400: {"model": ErrorResponse,"description": "訂單建立失敗，輸入不正確或其他原因"},
              403: {"model": ErrorResponse, "description": "未登入系統，拒絕存取"},
              500: {"model": ErrorResponse, "description": "伺服器內部錯誤"}
})

async def post_order(order: Order, credentials: HTTPBasicCredentials = Depends(http_bearer)):

    try:
        token = credentials.credentials
        email = await get_current_user(token)
        # print(email)

        if not email:
            raise HTTPException(status_code=403, detail="未登入系統")

        buyer_name = order.order.contact.name
        buyer_email = order.order.contact.email
        buyer_phone = order.order.contact.phone
        order_price = order.order.price
        order_date = order.order.trip.date
        order_time = order.order.trip.time
        attr_id = order.order.trip.attraction.id
        attr_name = order.order.trip.attraction.name
        attr_addr = order.order.trip.attraction.address
        attr_img = order.order.trip.attraction.image

        cnxpool = mysql.connector.pooling.MySQLConnectionPool(**dbconfig)
        cnx = cnxpool.get_connection()
        cursor = cnx.cursor()

        sql_string = "INSERT INTO orders(buyer_name, buyer_email, buyer_phone, order_price, order_date, order_time, attr_id, attr_name, attr_addr, attr_img) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"


        val = (buyer_name, buyer_email, buyer_phone, order_price, order_date, order_time, attr_id, attr_name, attr_addr, attr_img)

        cursor.execute(sql_string, val)
        cnx.commit()

        order_id = cursor.lastrowid

        
        date_format = "%Y%m%d%H%M%S"
        current_date = datetime.now().strftime(date_format)

        uid = uuid.uuid4().hex.upper()
        truncated_uid = uid[:8]
        order_number = f"{current_date}-{truncated_uid}"


        headers = {
            "Content-Type": "application/json",
            "x-api-key": TAPPAY_PARTNER_KEY
        }

        
        payload = {
            "prime": order.prime,
            "partner_key": TAPPAY_PARTNER_KEY,
            "merchant_id": "tppf_angel1997_GP_POS_2",
            "details": order.order.trip.attraction.name,
            "amount": order_price,
            "order_number": order_number,
            "cardholder": {
                "phone_number": buyer_phone,
                "name": buyer_name,
                "email":buyer_email
            },
            "remember": False
        } 

        tappay_response = requests.post(TAPPAY_API_URL, json=payload, headers=headers)

        result = tappay_response.json()
        order_number = result["order_number"]
        print(result)
        # # print(result.get("status"))
        # # print(result["rec_trade_id"])

        cnx = cnxpool.get_connection()
        cursor = cnx.cursor()
        print(result["status"])
        if result["status"] != 0:
            raise HTTPException(status_code=400, detail="訂單建立失敗")
        sql_string = "INSERT INTO paidlist(order_id, paid_status, order_number) VALUES (%s, %s, %s)"
        val = (order_id, 1, order_number)

        cursor.execute(sql_string, val)
        cnx.commit()
        cursor.close()
        cnx.close()


        return  {"data": {
            "number": order_number,
            "payment": {
                "status": 1,
                "message": "付款成功"
            }
        }}

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="伺服器內部錯誤")

    

@order.get("/order/{orderNumber}", summary = "根據訂單編號取得訂單資訊")
async def get_order(orderNumber, credentials: HTTPBasicCredentials = Depends(http_bearer)):
    try:
        token = credentials.credentials
        email = await get_current_user(token)
        print(email)

        if not email:
            raise HTTPException(status_code=403, detail="未登入系統")

        cnxpool = mysql.connector.pooling.MySQLConnectionPool(**dbconfig)
        cnx = cnxpool.get_connection() 
        cursor = cnx.cursor()
        sql_string = "SELECT o.*, p.* FROM orders o LEFT JOIN paidlist p ON o.id = p.order_id WHERE p.order_number = %s;"

        cursor.execute(sql_string, (orderNumber,))

        data = cursor.fetchone()

        cursor.close()
        cnx.close()

        print(data)

        if not data:
            return {"data": None}
        
        return JSONResponse(status_code=200, content={"data": {
            "number": data[15],
            "price": data[4],
            "trip": {
                "attraction": {
                    "id": data[7],
                    "name": data[8],
                    "address": data[9],
                    "image": data[10]
                },
                "date": data[5],
                "time": data[6],
                "contact": {
                    "name": data[1],
                    "email": data[2],
                    "phone": data[3]
                },
            "status": data[14] 
            }}})
    
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="伺服器內部錯誤")