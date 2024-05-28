from fastapi import APIRouter

order = APIRouter()


@order.post("/orders", summary= "建立新的訂單，並完成付款程序")
async def post_order():
    return True

@order.get("/order/{orderNumber}", summary = "根據訂單編號取得訂單資訊")
async def get_order(orderNumber):
    return True