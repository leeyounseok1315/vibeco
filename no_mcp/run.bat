@echo off
echo 🛒 최저가 검색 Agent 실행 중...
echo.
echo 📋 사전 준비사항:
echo 1. Python이 설치되어 있어야 합니다
echo 2. Gemini API 키가 설정되어 있어야 합니다
echo.
echo 🔑 API 키 설정 방법:
echo - 환경변수: set GEMINI_API_KEY=your_api_key
echo - 또는 .streamlit/secrets.toml 파일에 추가
echo.
echo 📦 의존성 설치 중...
pip install -r requirements.txt
echo.
echo 🚀 Streamlit 앱 실행 중...
streamlit run app.py
pause
