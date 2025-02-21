from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from data.db import Base  # 공통 데이터베이스 설정 불러오기

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(255), unique=True, index=True)
    email = Column(String(255), unique=True, index=True) # 데이터베이스 인덱스(index) 를 생성하여 검색 속도를 빠르게 하기 위한 설정
    password = Column(String(255))
#  history 테이블과의 1:N 관계 추가
    history = relationship("ObservationHistory", back_populates="user")