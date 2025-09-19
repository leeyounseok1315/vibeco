# 🛒 최저가 검색 Agent (MCP Context7 Enhanced)

사용자가 원하는 상품의 최저가를 인터넷에서 찾아서 가격과 구매사이트 링크를 리스트업해서 보여주는 AI Agent입니다. **MCP Context7 기술을 활용**하여 최신 Google GenAI SDK와 Gemini 2.5 Flash 모델을 사용합니다.

## ✨ 주요 기능

- **🤖 AI 기반 검색 전략**: Gemini 2.5 Flash를 활용한 스마트한 상품 검색 전략 수립
- **⚡ 비동기 검색**: aiohttp를 사용한 고성능 비동기 검색으로 빠른 결과 제공
- **💰 정확한 가격 비교**: 배송비, 쿠폰, 할인율을 모두 고려한 총 결제금액 비교
- **📊 고급 시각화**: Plotly를 사용한 인터랙티브 차트와 분석 도구
- **🔍 가격 분석 인사이트**: AI가 제공하는 구매 추천 전략
- **📱 반응형 UI**: Streamlit의 최신 기능을 활용한 모던한 인터페이스

## 🚀 MCP Context7 기술 활용

### 최신 Google GenAI SDK
- **라이브러리**: `google-genai` (최신 권장 라이브러리)
- **모델**: Gemini 2.5 Flash (최신 권장 모델)
- **API 버전**: v1alpha 지원으로 최신 기능 활용

### 비동기 검색 최적화
- **aiohttp**: 고성능 비동기 HTTP 클라이언트
- **asyncio**: Python 네이티브 비동기 프로그래밍
- **병렬 처리**: 여러 쇼핑몰 동시 검색으로 속도 향상

### AI 기반 검색 전략
- **동적 키워드 생성**: 상품별 최적화된 검색 키워드
- **사이트별 전략**: 각 쇼핑몰에 최적화된 검색 방법
- **가격 분석**: 할인율, 배송비, 쿠폰을 고려한 종합 분석

## 🛠️ 설치 및 실행

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
streamlit run main.py
```

브라우저에서 `http://localhost:8502`로 접속하면 됩니다.

## 🔑 Gemini API 키 발급 방법

1. [Google AI Studio](https://makersuite.google.com/app/apikey)에 접속
2. Google 계정으로 로그인
3. "Create API Key" 버튼 클릭
4. 생성된 API 키를 복사하여 위의 설정에 사용

## 📱 사용법

1. **상품명 입력**: 검색창에 찾고 싶은 상품명을 입력
2. **AI 전략 수립**: Gemini가 최적의 검색 전략을 자동으로 수립
3. **비동기 검색**: 여러 쇼핑몰에서 동시에 가격 정보 수집
4. **종합 분석**: 배송비, 쿠폰, 할인율을 모두 고려한 총 결제금액 비교
5. **구매 추천**: AI가 제공하는 최적의 구매 전략 확인

## 🏪 지원 쇼핑몰

- 쿠팡
- 11번가
- G마켓
- 옥션
- 인터파크
- 네이버쇼핑

## 🛠️ 기술 스택

### Backend
- **AI Model**: Google Gemini 2.5 Flash
- **SDK**: Google GenAI Python SDK (최신)
- **Async**: aiohttp, asyncio
- **Data Processing**: Pandas

### Frontend
- **Framework**: Streamlit
- **Visualization**: Plotly
- **UI Components**: Streamlit 최신 기능

### MCP Context7 Integration
- **최신 라이브러리 정보**: Google GenAI SDK 최신 버전 활용
- **모델 선택**: Gemini 2.5 Flash (권장 모델)
- **API 최적화**: 최신 권장사항 적용

## 📁 프로젝트 구조

```
with_mcp/
├── main.py                 # 메인 Streamlit 앱 (MCP Context7 Enhanced)
├── requirements.txt        # Python 의존성 (최신 라이브러리)
├── .streamlit/
│   └── config.toml       # Streamlit 설정 (포트 8502)
└── README.md             # 프로젝트 설명서
```

## 🔧 MCP Context7 기술적 특징

### 1. 최신 Google GenAI SDK
```python
# 기존 (deprecated)
import google.generativeai as genai
genai.configure(api_key=api_key)

# 최신 (MCP Context7 권장)
from google import genai
client = genai.Client(api_key=api_key)
```

### 2. Gemini 2.5 Flash 모델
```python
# 최신 권장 모델 사용
response = client.models.generate_content(
    model='gemini-2.5-flash',  # 최신 권장 모델
    contents=prompt,
    config=types.GenerateContentConfig(
        response_mime_type="application/json"
    )
)
```

### 3. 비동기 검색 최적화
```python
# aiohttp를 사용한 비동기 검색
async def search_all_sites_async(product_name, strategy):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for site in strategy["search_sites"]:
            task = search_site_async(session, site, product_name, strategy["search_keywords"])
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return results
```

## 📊 고급 시각화 기능

### 1. 가격 비교 차트
- **막대 차트**: 사이트별 총 결제금액 비교
- **산점도**: 할인율 vs 신뢰도 분석
- **파이 차트**: 할인율 분포 비교

### 2. 가격 분석 인사이트
- **통계 메트릭**: 평균 가격, 가격 범위, 평균 할인율
- **히스토그램**: 가격 분포 분석
- **구매 추천**: AI 기반 최적 구매 전략

## 🔧 커스터마이징

### 새로운 쇼핑몰 추가
`search_product_prices_ai` 함수의 `search_sites` 리스트에 새로운 쇼핑몰을 추가할 수 있습니다.

### 실제 크롤링 구현
현재는 시뮬레이션된 데이터를 사용하지만, 실제 구현 시에는 `search_site_async` 함수에서 각 쇼핑몰의 웹페이지를 크롤링하여 실시간 가격 정보를 가져올 수 있습니다.

### AI 전략 커스터마이징
`search_product_prices_ai` 함수의 프롬프트를 수정하여 AI의 검색 전략을 커스터마이징할 수 있습니다.

## ⚠️ 주의사항

- Gemini API 사용량에 따라 비용이 발생할 수 있습니다
- 실제 상품 가격은 시뮬레이션된 데이터이므로 참고용으로만 사용하세요
- 상업적 용도로 사용 시 각 쇼핑몰의 이용약관을 확인하세요
- MCP Context7 기술을 활용하여 최신 라이브러리와 모델을 사용합니다

## 🚀 성능 최적화

### 비동기 처리
- 여러 쇼핑몰 동시 검색으로 검색 시간 단축
- aiohttp를 사용한 고성능 HTTP 요청

### AI 모델 최적화
- Gemini 2.5 Flash 모델로 빠른 응답 시간
- JSON 응답 형식으로 파싱 성능 향상

### 메모리 효율성
- 세션 상태를 사용한 검색 히스토리 관리
- 효율적인 데이터 구조와 시각화

## 🤝 기여하기

버그 리포트나 기능 제안은 언제든 환영합니다! MCP Context7 기술을 활용한 개선사항도 함께 논의해보세요.

## 📄 라이선스

이 프로젝트는 교육 및 개인 사용 목적으로 제작되었습니다. MCP Context7 기술을 활용하여 최신 AI 기술을 적용했습니다.

## 🔗 관련 링크

- [Google AI Studio](https://makersuite.google.com/app/apikey)
- [Google GenAI Python SDK](https://github.com/googleapis/python-genai)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [MCP Context7](https://context7.com/)
