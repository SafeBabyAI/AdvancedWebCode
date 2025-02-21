from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from data.user import User
from data.db import get_db
from service.utility import verify_password
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
import os

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

ALGORITHM = "HS256"  # JWT 암호화 알고리즘
ACCESS_TOKEN_EXPIRE_MINUTES = 3 * 24 * 60  # 토큰 유효기간 (3일)

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")  

# Pydantic 모델을 사용하여 요청 데이터 형식 지정
class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login/")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == request.username).first()

    if not user:
        raise HTTPException(status_code=401, detail="아이디가 존재하지 않습니다.")
    
    if not verify_password(request.password, user.password):
        raise HTTPException(status_code=401, detail="비밀번호가 틀렸습니다.")
    
    # JWT 토큰 생성 및 발급 
    access_token = jwt.encode(
        {
         "sub": user.username, 
         "user_id": user.id, 
         "exp": datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        },
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return {"access_token": access_token, "token_type": "bearer"}

#현재 로그인된 사용자의 user_id 가져오는 함수 
def get_current_user_id(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")  # token발급 시 저장했던 user_id 가져오기

        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return user.id  # 로그인된 사용자의 id 반환

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


@router.get("/user/me")
async def get_user_info(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "username": user.username,
        "email": user.email,
        "id": user.id,
    }
