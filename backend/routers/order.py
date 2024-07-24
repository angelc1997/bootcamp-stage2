from datetime import datetime, timedelta, timezone
import json
from typing import Annotated, List, Optional, Union
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPBasicCredentials
from pydantic import BaseModel, EmailStr
import jwt
from jwt.exceptions import InvalidTokenError
import requests
import uuid 
from datetime import datetime

from ..models.User import UserModel
from ..models.Order import OrderModel
from src.tappay import tappaytoken

order = APIRouter()
http_bearer = HTTPBearer()

TAPPAY_PARTNER_KEY = tappaytoken["TAPPAY_PARTNER_KEY"]
TAPPAY_API_URL = tappaytoken["TAPPAY_API_URL"]


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




@order.post("/orders", summary= "建立新的訂單，並完成付款程序", responses={
              400: {"model": ErrorResponse,"description": "訂單建立失敗，輸入不正確或其他原因"},
              403: {"model": ErrorResponse, "description": "未登入系統，拒絕存取"},
              500: {"model": ErrorResponse, "description": "伺服器內部錯誤"}
})

async def post_order(order: Order, credentials: HTTPBasicCredentials = Depends(http_bearer)):

    try:
        token = credentials.credentials
        email = await UserModel.get_current_user(token)
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

        order_id = OrderModel.insert_order(buyer_name, buyer_email, buyer_phone, order_price, order_date, order_time, attr_id, attr_name, attr_addr, attr_img)

        
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
       
        if result["status"] != 0:
            raise HTTPException(status_code=400, detail="訂單建立失敗")
        
        insert_paidlist = OrderModel.insert_paidlist(order_id, 1, order_number)

        if insert_paidlist:
            return  {"data": {
                "number": order_number,
                "payment": {
                    "status": 1,
                    "message": "付款成功"
                }
        }}

    except Exception as e:
        raise HTTPException(status_code=500, detail="伺服器內部錯誤")

    

@order.get("/order/{orderNumber}", summary = "根據訂單編號取得訂單資訊")
async def get_order(orderNumber, credentials: HTTPBasicCredentials = Depends(http_bearer)):
    try:
        token = credentials.credentials
        email = await UserModel.get_current_user(token)
        print(email)

        if not email:
            raise HTTPException(status_code=403, detail="未登入系統")

        data = OrderModel.get_paid_order(orderNumber)

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
        raise HTTPException(status_code=500, detail="伺服器內部錯誤")