from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPBasicCredentials
from pydantic import BaseModel, EmailStr
from ..models.User import UserModel
from ..models.Book import BookModel

book = APIRouter()
http_bearer = HTTPBearer()


class SuccessResponse(BaseModel):
    ok: bool = True

class ErrorResponse(BaseModel):
    error: bool = True
    message: str = "請按照情境提供對應的錯誤訊息"

class BookingPost(BaseModel):
    attractionId: int = 10
    date: str = "2022/01/31"
    time: str  = "afternoon"
    price: int = 2500

class Attraction(BaseModel):
    id: int = 10
    name: str = "平安鐘"
    address: str = "臺北市大安區忠孝東路 4 段"
    image: str = "https://yourdomain.com/images/attraction/10.jpg"


class BookingInfo(BaseModel):
    attraction: Attraction
    date: str = "2022-01-31"
    time: str = "afternoon"
    price: int = 2000

class BookingInfoList(BaseModel):
    data: BookingInfo

@book.get("/booking", summary= "取得尚未確認下單的預定行程", responses={
    200: {"model": BookingInfoList, "description": "尚未確認下單的預定行程資料，null 表示沒有資料"},
    403: {"model": ErrorResponse, "description": "未登入系統，拒絕存取"}
})
async def get_booking(credentials: HTTPBasicCredentials = Depends(http_bearer)):
    try:
        token = credentials.credentials
        email = await UserModel.get_current_user(token)
        
        data = UserModel.get_user(email)   

        if not data:
            raise HTTPException(status_code=400, detail="未登入")
        
        # 獲取預定行程資訊
        booking = BookModel.book_data(data[0])

        if not booking:
            return {"data": None}

        booking = {
            "data": {
                "attraction" : {
                    "id": booking[3],
                    "name": booking[4],
                    "address": booking[5],
                    "image": booking[6].split(",")[0]
                },
                "date": booking[0],
                "time": booking[1],
                "price": booking[2]
                }
        }
            

        return booking

       

    except Exception as e:
        # print(e)
        raise HTTPException(status_code=500, detail="伺服器內部錯誤")

@book.post("/booking", summary= "建立新的預定行程", responses={
    200: {"model": BookingPost, "description": "建立成功"},
    400: {"model": ErrorResponse, "description": "建立失敗，輸入不正確或其他原因"},
    403: {"model": ErrorResponse, "description": "未登入系統，拒絕存取"}
})
async def post_booking(form: BookingPost, credentials: HTTPBasicCredentials = Depends(http_bearer)):
    try:
        token = credentials.credentials
        email = await UserModel.get_current_user(token)

        existing_user = UserModel.get_user(email)
        
        if not existing_user:
            raise HTTPException(status_code=403, detail="未登入")
        
        if not form.date:
            raise HTTPException(status_code=400, detail="請輸入日期")
        
        if not form.time:
            raise HTTPException(status_code=400, detail="請輸入時間")
        
        if not form.price:
            raise HTTPException(status_code=400, detail="請輸入價格")

        # 插入預定行程資訊
        result = BookModel.insert_booking(
            member_id=existing_user[0], 
            attr_id=form.attractionId, 
            date=form.date, 
            time=form.time, 
            price=form.price
        )

        if not result:
            raise HTTPException(status_code=500, detail="伺服器內部錯誤")

        return {"attractionId": form.attractionId, "date": form.date, "time": form.time, "price": form.price}
    

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="伺服器內部錯誤")

    

@book.delete("/booking", summary= "刪除目前的預定行程", responses={
    200: {"model": SuccessResponse, "description": "刪除成功"},
    403: {"model": ErrorResponse, "description": "未登入系統，拒絕存取"}
})
async def delete_booking(credentials: HTTPBasicCredentials = Depends(http_bearer)):
    try: 
        token = credentials.credentials
        email = await UserModel.get_current_user(token)
        
        data = UserModel.get_user(email)

        if not data:
            raise ErrorResponse(message="未登入")
        
        #  刪除預定行程資訊
        result = BookModel.delete_booking(data[0])
        if not result:
            raise HTTPException(status_code=500, detail="伺服器內部錯誤")

        return {"ok": True}
    
    except Exception as e:
        # print(e)
        raise HTTPException(status_code=500, detail="伺服器內部錯誤")


