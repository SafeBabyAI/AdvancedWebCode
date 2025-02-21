from sqlalchemy import Column, Integer, String
from database import Base  # 공통 데이터베이스 설정 불러오기

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, index=True)
    email = Column(String(255), unique=True, index=True)
    password = Column(String(255))
