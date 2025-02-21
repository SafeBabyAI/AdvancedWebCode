from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from sqlalchemy import cast, Date
from data.db import get_db
from pydantic import BaseModel
import os, json
from data.history import ObservationHistory
from dotenv import load_dotenv
from data.imgdb import download_images_from_blob
import base64

# 환경 변수 로드
load_dotenv()
AZURE_STORAGE_CONNECTION_STRING = os.getenv("CONNECTION_STRING")
AZURE_CONTAINER_NAME="safe13aby"

router = APIRouter()

class HistorySearchRequest(BaseModel):
    date: str 

@router.post("/history/images")
def get_images_by_date(request: HistorySearchRequest, db: Session = Depends(get_db)):
    """특정 날짜의 감지 기록을 조회하고, 해당하는 이미지들을 클라이언트에 반환"""
    try:
        history_records = (
            db.query(ObservationHistory.timestamp, ObservationHistory.duration, 
                     ObservationHistory.observed_info, ObservationHistory.image_url)
            .filter(cast(ObservationHistory.timestamp, Date) == request.date)  # 날짜 비교
            .order_by(ObservationHistory.timestamp.desc())
            .all()
        )
        if not history_records:
            raise HTTPException(status_code=404, detail="선택한 날짜에 감지된 기록이 없습니다.")
        
        # Blob Storage에서 해당 날짜의 이미지 다운로드
        images = download_images_from_blob(request.date)
        # print(f"가져온 이미지 수: {len(images)}")

        if not images:
            raise HTTPException(status_code=404, detail="이미지를 찾을 수 없습니다.")
        
        # 이미지 URL을 키로 하는 딕셔너리 생성 (Blob Storage에서 다운로드한 이미지 데이터)
        image_map = {img["url"]: base64.b64encode(img["image"]).decode("utf-8") for img in images}

        response_data = [
            {
                "image_base64": image_map.get(record.image_url, None),  # Blob에서 받은 Base64 이미지
                "url": record.image_url,  # 이미지 URL
                "timestamp": record.timestamp.strftime("%Y-%m-%d %H:%M:%S"),  # 시간 변환
                "duration": record.duration,  # 지속 시간
                "observed_info": record.observed_info  # 관찰된 정보
            }
            for record in history_records
        ]
        return Response(content=json.dumps(response_data), media_type="application/json")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"서버 오류: {str(e)}")