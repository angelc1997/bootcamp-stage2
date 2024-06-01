from fastapi import APIRouter

book = APIRouter()

@book.get("/booking", summary= "取得尚未確認下單的預定行程")
async def get_booking():
    return True

@book.post("/booking", summary= "建立新的預定行程")
async def post_booking():
    return True


@book.delete("/booking", summary= "刪除目前的預定行程")
async def delete_booking():
    return True