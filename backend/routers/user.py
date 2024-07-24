from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPBasicCredentials
from pydantic import BaseModel, EmailStr
from ..models.User import UserModel

http_bearer = HTTPBearer()

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
    name: str = "test"
    email: EmailStr ="test@gmail.com"

class UserAuthInfoObject(BaseModel):
    data: UserAuthInfo



@user.post("/user", summary="註冊一個新的會員", responses={
              200: {"model": SuccessResponse, "description": "註冊成功"},
              400: {"model": ErrorResponse,"description": "註冊失敗，重複的 Email 或其他原因"},
              500: {"model": ErrorResponse, "description": "伺服器內部錯誤"}})

async def post_user(user: SignUpUser):
    try:
        name = user.name
        email = user.email
        password = user.password

        existing_user = UserModel.get_user(email)
        
        if existing_user:
            return ErrorResponse(message="此信箱已被註冊")
        
        password = UserModel.get_password_hash(password)
        create_user_result = UserModel.create_user(name, email, password)

        if not create_user_result:
            return ErrorResponse(message="註冊失敗")
        
        return SuccessResponse(ok=True)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="伺服器內部錯誤")
    
@user.get("/user/auth", summary="取得當前登入的會員資訊", responses={
    200: {"model": UserAuthInfoObject, "description": "已登入的會員資料，null 表示未登入"},
})
async def get_decode_token(credentials: HTTPBasicCredentials = Depends(http_bearer)):

    try:
        token = credentials.credentials
        email = await UserModel.get_current_user(token)
        data = UserModel.get_user(email)

        if data:
            user_info = UserAuthInfo(id=data[0], name=data[1], email=data[2])
            return {"data": user_info}
        else:
            return {"data": None}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="伺服器內部錯誤")
    

@user.put("/user/auth", summary="登入會員帳戶", responses={
    200: {"model": SignInResponse, "description": "登入成功，得有效期為七天的 JWT 加密字串"},
    400: {"model": ErrorResponse, "description": "登入失敗，帳號或密碼錯誤或其他原因"},
    500: {"model": ErrorResponse, "description": "伺服器內部錯誤"}
})
async def get_encode_token(user: SignInUser):
    try:
        email = user.email
        password = user.password

        authenticated_user = UserModel.authenticate_user(email, password)

        if not authenticated_user:
           return ErrorResponse(message="帳號或密碼錯誤")
        
        access_token_expires = timedelta(days=7)
        access_token = UserModel.create_access_token(
            data={"sub": authenticated_user[2]},
            expires_delta=access_token_expires
        )

        # 紀錄使用者的TOKEN
        token_result = UserModel.update_token(email, access_token)

        if not token_result:
            raise HTTPException(status_code=500, detail="伺服器內部錯誤")
        
        return SignInResponse(token=access_token)

    except Exception as e:
        raise HTTPException(status_code=500, detail="伺服器內部錯誤")
    

    