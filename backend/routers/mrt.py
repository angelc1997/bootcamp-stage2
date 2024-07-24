from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from ..models.Mrt import MrtModel


mrt = APIRouter()


class SuccessResponse(BaseModel):
    data: List[str] = ["劍潭"] 


class ErrorResponse(BaseModel):
    error: bool = True
    message: str = "請按照情境提供對應的錯誤訊息"



@mrt.get("/mrts", 
         summary="取得捷運站名稱列表", 
         description="取得所有捷運站名稱列表，按照週邊景點的數量由大到小排序", 
         responses={
             200: {"model": SuccessResponse, "description": "正常運作"},
             500: {"model": ErrorResponse, "description": "伺服器內部錯誤"}
         })


async def get_mrts():


    try:
        data = MrtModel.mrt_list()
       
        # print(data)
        data = [i[0] for i in data]
        return {"data": data}

    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": True, "message": "伺服器內部錯誤"})