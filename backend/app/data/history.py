from sqlalchemy import Column, Integer, Text, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from data.db import Base  # 공통 데이터베이스 설정 불러오기
import json

class ObservationHistory(Base): # Base 상속
    __tablename__ = "history"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Azure Blob Storage에 저장된 이미지의 URL을 저장
    image_url = Column(String(500), nullable=False)  

    # Date + Time을 하나의 칼럼으로 저장
    timestamp = Column(DateTime, nullable=False)  

    duration = Column(Integer, nullable=False)

    observed_info = Column(Text, nullable=False)  # JSON 데이터를 TEXT로 저장

    # user_id 컬럼 추가 (users 테이블의 id를 참조하는 외래 키)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # User 모델과 관계 설정 (1:N 관계)
    user = relationship("User", back_populates="history")  # ORM 관계 설정

    def to_dict(self):
        """객체를 딕셔너리 형태로 변환 (JSON 변환 용이)"""
        return {
            "id": self.id,
            "image_url": self.image_url,
            "timestamp": self.timestamp.isoformat(),
            "duration": self.duration,
            "observed_info": json.loads(self.observed_info),  # JSON 문자열 → Python dict 변환
            "user_id": self.user_id  # 🔹 추가된 user_id 포함
        }

    @classmethod  # @classmethod는 클래스 자체를 첫 번째 인자로 받는 메서드.
    def from_dict(cls, data):
        """딕셔너리 데이터를 SQLAlchemy 객체로 변환"""
        return cls(
            image_url=data["image_url"],
            timestamp=data["timestamp"],
            duration=data["duration"],
            observed_info=json.dumps(data["observed_info"]),  # Python dict → JSON 문자열 변환
            user_id=data["user_id"]
        )
    
   