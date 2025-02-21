import os,io
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient

# 환경 변수 로드
load_dotenv()
# Azure Storage 연결 문자열
AZURE_STORAGE_CONNECTION_STRING = os.getenv("CONNECTION_STRING")
# Azure Blob 컨테이너 이름
AZURE_CONTAINER_NAME="safe13aby"


# Blob 서비스 클라이언트 생성
blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)

def upload_image_to_blob(image, blob_name):
    """ 이미지를 Azure Blob Storage에 업로드하고, 업로드된 URL을 반환하는 함수. """
    try:
        # 컨테이너 클라이언트 가져오기
        container_client = blob_service_client.get_container_client(AZURE_CONTAINER_NAME)

        if not container_client.exists():
            container_client.create_container()
        # 이미지 데이터를 바이트 스트림으로 변환

        image_stream = io.BytesIO()
        image.save(image_stream, format="JPEG")  # JPEG 형식으로 저장
        image_stream.seek(0)  # 스트림 시작 위치로 이동

        # Blob 업로드
        blob_client = container_client.get_blob_client(blob_name)
        blob_client.upload_blob(image_stream, blob_type="BlockBlob", overwrite=True)

        # 업로드된 Blob의 URL 반환
        blob_url = f"https://{blob_service_client.account_name}.blob.core.windows.net/{AZURE_CONTAINER_NAME}/{blob_name}"
        return blob_url
    
    except Exception as e:
        print(f"Azure Blob Storage 업로드 실패: {e}")
        return None

def download_images_from_blob(requested_date):
    """특정 날짜(YYYYMMDD)와 일치하는 모든 파일을 다운로드."""
    images = []
    try:
        container_client = blob_service_client.get_container_client(AZURE_CONTAINER_NAME)
        #print(f"컨테이너 연결 확인: {AZURE_CONTAINER_NAME}, 존재 여부: {container_client.exists()}")
        requested_date = requested_date.replace("-", "")  # "2025-02-21" → "20250221"(YYYY-MM-DD → YYYYMMDD)

        # 존재하는 블롭 파일 목록 가져오기
        blobs = container_client.list_blobs()
        existing_blob_names = [blob.name for blob in blobs]  # 블롭 목록을 리스트로 저장
        matching_blobs = [blob for blob in existing_blob_names if blob.split("/")[-1].startswith(requested_date)] # 파일 찾기
 
        if not matching_blobs:
            print(f"해당 날짜({requested_date})에 대한 파일이 없습니다.")
            return []

        for blob_name in matching_blobs:
            try:
                # Blob 파일 다운로드
                blob_client = container_client.get_blob_client(blob_name)
                blob_data = blob_client.download_blob().readall()

                if not blob_data:
                    print(f"다운로드 실패: {blob_name} (빈 데이터)")
                    continue  # 빈 데이터라면 추가하지 않음

                image_url = f"https://{blob_service_client.account_name}.blob.core.windows.net/{AZURE_CONTAINER_NAME}/{blob_name}"
                images.append({"image": blob_data, "url": image_url})

            except Exception as e:
                print(f"다운로드 중 오류 발생: {blob_name}, 오류: {e}")

        print(f"다운로드 완료! 총 {len(images)}개 파일을 가져왔습니다.")
        return images  # ✅ 특정 날짜의 모든 이미지 데이터 반환

    except Exception as e:
        print(f"Azure Blob Storage 다운로드 실패: {e}")
        return None
