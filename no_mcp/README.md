# 🛒 최저가 검색 Agent

사용자가 원하는 상품의 최저가를 인터넷에서 찾아서 가격과 구매사이트 링크를 리스트업해서 보여주는 AI Agent입니다.

## ✨ 주요 기능

- **AI 기반 상품 검색**: Gemini AI를 활용한 스마트한 상품 검색
- **최저가 비교**: 여러 쇼핑몰의 가격을 비교하여 최저가 제공
- **시각화**: 차트와 그래프를 통한 직관적인 가격 비교
- **구매 링크**: 각 쇼핑몰의 직접 구매 링크 제공
- **검색 히스토리**: 이전 검색 결과 저장 및 관리

## 🚀 설치 및 실행

### 1. 의존성 설치

```bash
pip install -r requirements.txt
```

### 2. Gemini API 키 설정

#### 방법 1: 환경변수 설정
```bash
# Windows
set GEMINI_API_KEY=your_api_key_here

# macOS/Linux
export GEMINI_API_KEY=your_api_key_here
```

#### 방법 2: Streamlit secrets 설정
`.streamlit/secrets.toml` 파일을 생성하고 다음 내용을 추가:
```toml
GEMINI_API_KEY = "your_api_key_here"
```

### 3. 앱 실행

```bash
streamlit run app.py
```

브라우저에서 `http://localhost:8501`로 접속하면 됩니다.

## 🔑 Gemini API 키 발급 방법

1. [Google AI Studio](https://makersuite.google.com/app/apikey)에 접속
2. Google 계정으로 로그인
3. "Create API Key" 버튼 클릭
4. 생성된 API 키를 복사하여 위의 설정에 사용

## 📱 사용법

1. **상품명 입력**: 검색창에 찾고 싶은 상품명을 입력
2. **검색 실행**: "🔍 검색" 버튼 클릭
3. **결과 확인**: AI가 찾은 최저가와 가격 비교 결과 확인
4. **구매 링크**: 원하는 쇼핑몰의 링크 클릭하여 구매

## 🏪 지원 쇼핑몰

- 쿠팡
- 11번가
- G마켓
- 옥션
- 인터파크
- 티몬
- 위메프
- 네이버쇼핑
- 카카오톡 선물하기

## 🛠️ 기술 스택

- **Frontend**: Streamlit
- **AI Model**: Google Gemini Pro
- **Data Processing**: Pandas
- **Visualization**: Plotly
- **Web Scraping**: BeautifulSoup4, Requests

## 📁 프로젝트 구조

```
no_mcp/
├── app.py                 # 메인 Streamlit 앱
├── requirements.txt       # Python 의존성
├── .streamlit/
│   └── config.toml      # Streamlit 설정
├── index.html            # 시작 페이지
└── README.md            # 프로젝트 설명서
```

## 🔧 커스터마이징

### 새로운 쇼핑몰 추가
`simulate_price_search` 함수의 `sites` 리스트에 새로운 쇼핑몰을 추가할 수 있습니다.

### 실제 크롤링 구현
현재는 시뮬레이션된 데이터를 사용하지만, 실제 구현 시에는 각 쇼핑몰의 웹페이지를 크롤링하여 실시간 가격 정보를 가져올 수 있습니다.

## ⚠️ 주의사항

- Gemini API 사용량에 따라 비용이 발생할 수 있습니다
- 실제 상품 가격은 시뮬레이션된 데이터이므로 참고용으로만 사용하세요
- 상업적 용도로 사용 시 각 쇼핑몰의 이용약관을 확인하세요

## 🤝 기여하기

버그 리포트나 기능 제안은 언제든 환영합니다!

## 📄 라이선스

이 프로젝트는 교육 및 개인 사용 목적으로 제작되었습니다.
