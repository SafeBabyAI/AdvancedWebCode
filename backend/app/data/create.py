from db import engine, Base
from user import User
from history import ObservationHistory

# 모든 테이블을 생성
Base.metadata.create_all(bind=engine)
