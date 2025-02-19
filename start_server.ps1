# FastAPI 백엔드 실행
Start-Process -NoNewWindow -FilePath "cmd.exe" -ArgumentList "/c cd backend\app && ..\.venv\Scripts\activate && uvicorn main:app --host 0.0.0.0 --port 8000 --reload"

# Vue.js 프론트엔드 실행
Start-Process -NoNewWindow -FilePath "cmd.exe" -ArgumentList "/c cd frontend && npm run dev"

# 빌드 결과를 로컬 서버에서 미리보기 : npm run preview