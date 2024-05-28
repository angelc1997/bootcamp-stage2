from fastapi import APIRouter

user = APIRouter()


@user.post("/user", summary="註冊一個新的會員")
async def post_user():
    return True

@user.get("/user/auth", summary="取得當前登入的會員資訊")
async def get_user_auth():
    return True


@user.put("/user/auth", summary="登入會員帳戶")
async def put_user_auth():
    return True