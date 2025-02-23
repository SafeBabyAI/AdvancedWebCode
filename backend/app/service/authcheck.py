from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from dotenv import load_dotenv
import os

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")  
# 클라이언트가 Authorization: Bearer <토큰> 헤더를 통해 토큰을 제공해야 함을 의미

@router.get("/check")
async def check_authentication(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) # 토큰을 디코딩하여 유효성을 검증
        return {"message": "Authenticated", "username": payload.get("sub")}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
