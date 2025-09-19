import streamlit as st
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime
import os

# 페이지 설정
st.set_page_config(
    page_title="최저가 검색 Agent",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Gemini API 설정
def setup_gemini():
    """Gemini API 설정"""
    api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        st.error("⚠️ Gemini API 키가 설정되지 않았습니다.")
        st.info("""
        API 키를 설정하는 방법:
        1. 환경변수로 설정: `GEMINI_API_KEY=your_api_key`
        2. Streamlit secrets로 설정: `.streamlit/secrets.toml` 파일에 `GEMINI_API_KEY = "your_api_key"` 추가
        """)
        return None
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        return model
    except Exception as e:
        st.error(f"Gemini API 설정 오류: {e}")
        return None

def search_product_prices(product_name, model):
    """상품 가격 검색 및 분석"""
    try:
        # Gemini에게 상품 검색 전략 요청
        prompt = f"""
        다음 상품의 최저가를 찾기 위한 검색 전략을 제시해주세요:
        상품명: {product_name}
        
        다음 형식으로 응답해주세요:
        {{
            "search_keywords": ["검색할 키워드1", "검색할 키워드2"],
            "search_sites": ["검색할 사이트1", "검색할 사이트2"],
            "price_analysis": "가격 분석 방법 설명"
        }}
        """
        
        response = model.generate_content(prompt)
        strategy = json.loads(response.text)
        
        # 실제 검색 시뮬레이션 (실제로는 각 사이트에서 크롤링 필요)
        mock_results = simulate_price_search(product_name, strategy)
        
        return mock_results
        
    except Exception as e:
        st.error(f"상품 검색 중 오류 발생: {e}")
        return None

def simulate_price_search(product_name, strategy):
    """가격 검색 시뮬레이션 (실제 구현 시에는 실제 크롤링으로 대체)"""
    import random
    
    # 시뮬레이션된 검색 결과
    sites = [
        "쿠팡", "11번가", "G마켓", "옥션", "인터파크", 
        "티몬", "위메프", "네이버쇼핑", "카카오톡 선물하기"
    ]
    
    results = []
    base_price = random.randint(10000, 100000)
    
    for i, site in enumerate(sites[:6]):  # 상위 6개 사이트만
        price = base_price + random.randint(-5000, 5000)
        if price < 0:
            price = random.randint(5000, 15000)
        
        discount = random.randint(0, 30)
        final_price = int(price * (1 - discount/100))
        
        results.append({
            "site": site,
            "original_price": f"{price:,}원",
            "discount": f"{discount}%",
            "final_price": f"{final_price:,}원",
            "link": f"https://{site.lower()}.com/search?q={product_name}",
            "rating": round(random.uniform(3.5, 5.0), 1),
            "reviews": random.randint(10, 1000)
        })
    
    # 가격순으로 정렬
    results.sort(key=lambda x: int(x["final_price"].replace(",", "").replace("원", "")))
    
    return results

def display_price_results(results, product_name):
    """가격 검색 결과 표시"""
    if not results:
        st.warning("검색 결과가 없습니다.")
        return
    
    st.subheader(f"🎯 '{product_name}' 최저가 검색 결과")
    
    # 최저가 하이라이트
    best_price = results[0]
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown(f"""
        <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    border-radius: 15px; color: white; margin: 20px 0;">
            <h3>🏆 최저가</h3>
            <h2>{best_price['final_price']}</h2>
            <p>{best_price['site']} | {best_price['original_price']} → {best_price['discount']} 할인</p>
        </div>
        """, unsafe_allow_html=True)
    
    # 전체 결과 테이블
    st.subheader("📊 전체 가격 비교")
    
    # 결과를 데이터프레임으로 변환
    import pandas as pd
    
    df_data = []
    for result in results:
        df_data.append({
            "순위": len(df_data) + 1,
            "사이트": result["site"],
            "최종가격": result["final_price"],
            "원가": result["original_price"],
            "할인율": result["discount"],
            "평점": result["rating"],
            "리뷰수": result["reviews"],
            "링크": result["link"]
        })
    
    df = pd.DataFrame(df_data)
    
    # 스타일링된 테이블 표시
    st.dataframe(
        df,
        column_config={
            "링크": st.column_config.LinkColumn("구매 링크"),
            "평점": st.column_config.NumberColumn("평점", format="%.1f"),
            "리뷰수": st.column_config.NumberColumn("리뷰수", format="%d")
        },
        hide_index=True,
        use_container_width=True
    )
    
    # 차트로 시각화
    st.subheader("📈 가격 비교 차트")
    
    import plotly.express as px
    
    # 가격 데이터 준비
    chart_data = []
    for result in results:
        price = int(result["final_price"].replace(",", "").replace("원", ""))
        chart_data.append({
            "사이트": result["site"],
            "가격": price,
            "할인율": int(result["discount"].replace("%", ""))
        })
    
    # 가격 비교 막대 차트
    fig_price = px.bar(
        chart_data, 
        x="사이트", 
        y="가격",
        title="사이트별 가격 비교",
        color="가격",
        color_continuous_scale="viridis"
    )
    fig_price.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_price, use_container_width=True)
    
    # 할인율 비교 차트
    fig_discount = px.pie(
        chart_data,
        values="할인율",
        names="사이트",
        title="사이트별 할인율 비교"
    )
    st.plotly_chart(fig_discount, use_container_width=True)

def main():
    st.title("🛒 최저가 검색 Agent")
    st.markdown("---")
    
    # 사이드바 설정
    with st.sidebar:
        st.header("⚙️ 설정")
        
        # Gemini 모델 설정
        model = setup_gemini()
        
        if model:
            st.success("✅ Gemini API 연결 성공")
        else:
            st.error("❌ Gemini API 연결 실패")
            return
        
        st.markdown("---")
        st.markdown("### 📋 사용법")
        st.markdown("""
        1. 검색할 상품명을 입력하세요
        2. 검색 버튼을 클릭하세요
        3. AI가 최저가를 찾아드립니다
        """)
        
        st.markdown("---")
        st.markdown("### 🔍 지원 사이트")
        st.markdown("""
        - 쿠팡
        - 11번가
        - G마켓
        - 옥션
        - 인터파크
        - 네이버쇼핑
        """)
    
    # 메인 컨텐츠
    if not model:
        st.error("Gemini API를 설정해주세요.")
        return
    
    # 검색 입력
    col1, col2 = st.columns([3, 1])
    
    with col1:
        product_name = st.text_input(
            "🔍 검색할 상품명을 입력하세요",
            placeholder="예: 삼성 갤럭시 S24, 애플 맥북 프로, 나이키 운동화...",
            help="구체적으로 입력할수록 정확한 결과를 얻을 수 있습니다."
        )
    
    with col2:
        search_button = st.button("🔍 검색", type="primary", use_container_width=True)
    
    st.markdown("---")
    
    # 검색 실행
    if search_button and product_name:
        with st.spinner("🔍 상품을 검색하고 있습니다..."):
            # 진행바 표시
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i in range(100):
                time.sleep(0.02)
                progress_bar.progress(i + 1)
                if i < 30:
                    status_text.text("🔍 상품 정보 수집 중...")
                elif i < 60:
                    status_text.text("💰 가격 정보 분석 중...")
                elif i < 90:
                    status_text.text("📊 결과 정리 중...")
                else:
                    status_text.text("✅ 검색 완료!")
            
            # 검색 결과 가져오기
            results = search_product_prices(product_name, model)
            
            if results:
                # 결과 표시
                display_price_results(results, product_name)
                
                # 검색 히스토리 저장 (세션 상태)
                if "search_history" not in st.session_state:
                    st.session_state.search_history = []
                
                st.session_state.search_history.append({
                    "product": product_name,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "best_price": results[0]["final_price"],
                    "best_site": results[0]["site"]
                })
                
                # 히스토리 표시
                with st.expander("📚 검색 히스토리"):
                    for item in reversed(st.session_state.search_history[-5:]):  # 최근 5개만
                        st.write(f"**{item['product']}** - {item['best_price']} ({item['best_site']}) - {item['timestamp']}")
            else:
                st.error("검색 결과를 가져올 수 없습니다.")
    
    elif not product_name and search_button:
        st.warning("⚠️ 검색할 상품명을 입력해주세요.")
    
    # 초기 화면
    if not search_button or not product_name:
        st.markdown("""
        <div style="text-align: center; padding: 40px;">
            <h2>🎯 최저가 검색 Agent에 오신 것을 환영합니다!</h2>
            <p style="font-size: 18px; color: #666;">
                원하는 상품의 최저가를 AI가 찾아드립니다.<br>
                위의 검색창에 상품명을 입력하고 검색해보세요!
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # 예시 상품들
        st.subheader("💡 인기 검색 상품 예시")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📱 스마트폰", use_container_width=True):
                st.session_state.example_product = "삼성 갤럭시 S24"
                st.rerun()
        
        with col2:
            if st.button("💻 노트북", use_container_width=True):
                st.session_state.example_product = "애플 맥북 프로"
                st.rerun()
        
        with col3:
            if st.button("👟 운동화", use_container_width=True):
                st.session_state.example_product = "나이키 운동화"
                st.rerun()
        
        # 예시 상품이 선택된 경우
        if "example_product" in st.session_state:
            st.info(f"💡 예시 상품 '{st.session_state.example_product}'이 선택되었습니다. 검색창에 입력되어 있습니다.")
            st.text_input("🔍 검색할 상품명을 입력하세요", value=st.session_state.example_product, key="example_input")
            if st.button("🔍 예시 상품 검색", type="primary"):
                del st.session_state.example_product
                st.rerun()

if __name__ == "__main__":
    main()
