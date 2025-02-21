from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from data.user import User
from data.db import get_db
from service.utility import hash_password

router = APIRouter()

# Pydantic 모델 추가
class SignupRequest(BaseModel):
    username: str
    email: str
    password: str

@router.post("/signup/")
def signup(request: SignupRequest, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter((User.username == request.username) | (User.email == request.email)).first()

    if existing_user: # 중복된 사용자인지 판별 
        raise HTTPException(status_code=400, detail="Username or email already registered")
    
    hashed_password = hash_password(request.password) # 해시값으로 변환 
    new_user = User(username=request.username, email=request.email, password=hashed_password)
    db.add(new_user)

    db.commit()

    db.refresh(new_user)
    return {"message": "User created successfully"}
