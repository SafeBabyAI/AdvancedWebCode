from sqlalchemy import Column, Integer, String, LargeBinary, Date, Time
from database import Base  # 공통 데이터베이스 설정 불러오기

class ObservationHistory(Base): # Base 상속속
    __tablename__ = "history"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    image = Column(LargeBinary, nullable=False)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    duration = Column(Integer, nullable=False)
    observed_info = Column(String, nullable=False)
