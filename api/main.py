"""
FastAPI 應用程式主檔案
提供使用者認證 API 端點
"""

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta
import jwt
from typing import Optional

# FastAPI 應用程式
app = FastAPI(
    title="Excel 資料清洗工具 API",
    description="提供使用者認證和資料處理功能",
    version="1.0.0"
)

# CORS 設定（允許前端跨域請求）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite 預設端口
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# JWT 設定
SECRET_KEY = "your-secret-key-change-this-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Pydantic 模型
class LoginRequest(BaseModel):
    """登入請求模型"""
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    """用戶回應模型"""
    id: str
    email: str
    name: Optional[str] = None

class TokenResponse(BaseModel):
    """Token 回應模型"""
    token: str
    user: UserResponse

class ErrorResponse(BaseModel):
    """錯誤回應模型"""
    message: str
    code: Optional[str] = None


# 模擬用戶資料庫（實際應用應使用真實資料庫）
MOCK_USERS = {
    "test@example.com": {
        "id": "1",
        "email": "test@example.com",
        "name": "測試用戶",
        "password": "password123"  # 實際應用應使用加密後的密碼
    },
    "admin@example.com": {
        "id": "2",
        "email": "admin@example.com",
        "name": "管理員",
        "password": "admin123"
    }
}


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """創建 JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


@app.get("/")
async def root():
    """API 根端點"""
    return {
        "message": "Excel 資料清洗工具 API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.post(
    "/api/auth/login",
    response_model=TokenResponse,
    responses={
        401: {"model": ErrorResponse, "description": "認證失敗"},
        422: {"model": ErrorResponse, "description": "驗證錯誤"}
    }
)
async def login(credentials: LoginRequest):
    """
    使用者登入端點

    驗證使用者憑證並返回 JWT token

    Args:
        credentials: 包含 email 和 password 的登入請求

    Returns:
        TokenResponse: 包含 JWT token 和用戶資料

    Raises:
        HTTPException: 認證失敗時拋出 401 錯誤
    """
    # 查找用戶
    user = MOCK_USERS.get(credentials.email)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="電子郵件或密碼錯誤"
        )

    # 驗證密碼（實際應用應使用 bcrypt 等安全方法）
    if user["password"] != credentials.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="電子郵件或密碼錯誤"
        )

    # 創建 access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"], "user_id": user["id"]},
        expires_delta=access_token_expires
    )

    # 返回 token 和用戶資料
    return TokenResponse(
        token=access_token,
        user=UserResponse(
            id=user["id"],
            email=user["email"],
            name=user.get("name")
        )
    )


@app.get("/api/health")
async def health_check():
    """健康檢查端點"""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
