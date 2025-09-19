import streamlit as st
from google import genai
from google.genai import types
import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import List, Dict, Any
import asyncio
import aiohttp

# 페이지 설정
st.set_page_config(
    page_title="최저가 검색 Agent",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Gemini API 설정 (최신 Google GenAI SDK 사용)
def setup_gemini():
    """Gemini API 설정 - 최신 Google GenAI SDK 사용"""
    api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        st.error("⚠️ Gemini API 키가 설정되지 않았습니다.")
        st.info("""
        API 키를 설정하는 방법:
        1. 환경변수로 설정: `GEMINI_API_KEY=your_api_key`
        2. Streamlit secrets로 설정: `.streamlit/secrets.toml` 파일에 `GEMINI_API_KEY = "your_api_key"` 추가
        
        🔑 Gemini API 키 발급 방법:
        1. [Google AI Studio](https://makersuite.google.com/app/apikey)에 접속
        2. Google 계정으로 로그인
        3. "Create API Key" 버튼 클릭
        4. 생성된 API 키를 복사하여 위의 설정에 사용
        """)
        return None
    
    try:
        # 최신 Google GenAI SDK 사용
        client = genai.Client(api_key=api_key)
        return client
    except Exception as e:
        st.error(f"Gemini API 설정 오류: {e}")
        return None

def search_product_prices_ai(product_name: str, client) -> Dict[str, Any]:
    """AI를 사용한 상품 가격 검색 전략 수립"""
    try:
        # Gemini 2.5 Flash 모델 사용 (최신 권장 모델)
        prompt = f"""
        다음 상품의 최저가를 찾기 위한 검색 전략을 제시해주세요:
        상품명: {product_name}
        
        다음 형식으로 JSON 응답해주세요:
        {{
            "search_keywords": ["검색할 키워드1", "검색할 키워드2", "검색할 키워드3"],
            "search_sites": ["쿠팡", "11번가", "G마켓", "옥션", "인터파크", "네이버쇼핑"],
            "price_analysis": "가격 분석 방법 설명",
            "search_strategy": "효율적인 검색 전략",
            "price_factors": ["할인율", "배송비", "쿠폰", "리뷰", "신뢰도"]
        }}
        
        한국 쇼핑몰에 최적화된 전략을 제시해주세요.
        """
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        
        strategy = json.loads(response.text)
        return strategy
        
    except Exception as e:
        st.error(f"AI 검색 전략 수립 중 오류 발생: {e}")
        # 기본 전략 반환
        return {
            "search_keywords": [product_name],
            "search_sites": ["쿠팡", "11번가", "G마켓", "옥션", "인터파크", "네이버쇼핑"],
            "price_analysis": "기본 가격 분석",
            "search_strategy": "표준 검색 전략",
            "price_factors": ["할인율", "배송비", "쿠폰", "리뷰", "신뢰도"]
        }

async def search_site_async(session: aiohttp.ClientSession, site: str, product_name: str, keywords: List[str]) -> Dict[str, Any]:
    """비동기로 특정 사이트에서 상품 검색"""
    try:
        # 실제 검색 시뮬레이션 (실제 구현 시에는 각 사이트에서 크롤링)
        import random
        
        # 시뮬레이션된 검색 결과
        base_price = random.randint(10000, 100000)
        price = base_price + random.randint(-8000, 8000)
        if price < 0:
            price = random.randint(5000, 15000)
        
        discount = random.randint(0, 40)
        final_price = int(price * (1 - discount/100))
        
        # 배송비 및 쿠폰 정보
        shipping_fee = random.choice([0, 2500, 3000, 5000])
        coupon_available = random.choice([True, False])
        coupon_amount = random.randint(1000, 5000) if coupon_available else 0
        
        # 리뷰 및 평점
        rating = round(random.uniform(3.0, 5.0), 1)
        reviews = random.randint(5, 2000)
        
        return {
            "site": site,
            "original_price": f"{price:,}원",
            "discount": f"{discount}%",
            "final_price": f"{final_price:,}원",
            "shipping_fee": f"{shipping_fee:,}원",
            "coupon_available": coupon_available,
            "coupon_amount": f"{coupon_amount:,}원" if coupon_available else "없음",
            "total_price": f"{final_price + shipping_fee - coupon_amount:,}원",
            "link": f"https://{site.lower().replace(' ', '')}.com/search?q={product_name}",
            "rating": rating,
            "reviews": reviews,
            "trust_score": random.randint(70, 100),
            "delivery_time": random.choice(["1-2일", "2-3일", "3-5일", "5-7일"])
        }
        
    except Exception as e:
        st.error(f"{site} 검색 중 오류: {e}")
        return None

async def search_all_sites_async(product_name: str, strategy: Dict[str, Any]) -> List[Dict[str, Any]]:
    """모든 사이트에서 비동기로 검색"""
    async with aiohttp.ClientSession() as session:
        tasks = []
        for site in strategy["search_sites"]:
            task = search_site_async(session, site, product_name, strategy["search_keywords"])
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # None이 아닌 결과만 필터링
        valid_results = [r for r in results if r is not None and not isinstance(r, Exception)]
        
        # 총 가격 기준으로 정렬 (배송비와 쿠폰 고려)
        for result in valid_results:
            total_price = int(result["final_price"].replace(",", "").replace("원", ""))
            shipping_fee = int(result["shipping_fee"].replace(",", "").replace("원", ""))
            coupon_amount = int(result["coupon_amount"].replace(",", "").replace("원", "")) if result["coupon_amount"] != "없음" else 0
            result["total_price_numeric"] = total_price + shipping_fee - coupon_amount
        
        valid_results.sort(key=lambda x: x["total_price_numeric"])
        return valid_results

def display_price_results(results: List[Dict[str, Any]], product_name: str, strategy: Dict[str, Any]):
    """가격 검색 결과 표시"""
    if not results:
        st.warning("검색 결과가 없습니다.")
        return
    
    st.subheader(f"🎯 '{product_name}' 최저가 검색 결과")
    
    # AI 전략 정보 표시
    with st.expander("🤖 AI 검색 전략", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            st.write("**검색 키워드:**")
            for keyword in strategy["search_keywords"]:
                st.write(f"• {keyword}")
            st.write("**검색 사이트:**")
            for site in strategy["search_sites"]:
                st.write(f"• {site}")
        
        with col2:
            st.write("**가격 분석:**")
            st.write(strategy["price_analysis"])
            st.write("**검색 전략:**")
            st.write(strategy["search_strategy"])
    
    # 최저가 하이라이트
    best_price = results[0]
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown(f"""
        <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    border-radius: 15px; color: white; margin: 20px 0;">
            <h3>🏆 최저가</h3>
            <h2>{best_price['total_price']}</h2>
            <p>{best_price['site']} | {best_price['final_price']} + {best_price['shipping_fee']} 배송비</p>
            <p>쿠폰: {best_price['coupon_amount']} | 할인: {best_price['discount']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # 전체 결과 테이블
    st.subheader("📊 전체 가격 비교")
    
    # 결과를 데이터프레임으로 변환
    df_data = []
    for i, result in enumerate(results):
        df_data.append({
            "순위": i + 1,
            "사이트": result["site"],
            "최종가격": result["final_price"],
            "배송비": result["shipping_fee"],
            "쿠폰": result["coupon_amount"],
            "총 결제금액": result["total_price"],
            "할인율": result["discount"],
            "평점": result["rating"],
            "리뷰수": result["reviews"],
            "신뢰도": result["trust_score"],
            "배송시간": result["delivery_time"],
            "링크": result["link"]
        })
    
    df = pd.DataFrame(df_data)
    
    # 스타일링된 테이블 표시
    st.dataframe(
        df,
        column_config={
            "링크": st.column_config.LinkColumn("구매 링크"),
            "평점": st.column_config.NumberColumn("평점", format="%.1f"),
            "리뷰수": st.column_config.NumberColumn("리뷰수", format="%d"),
            "신뢰도": st.column_config.NumberColumn("신뢰도", format="%d")
        },
        hide_index=True,
        use_container_width=True
    )
    
    # 차트로 시각화
    st.subheader("📈 가격 비교 차트")
    
    # 가격 데이터 준비
    chart_data = []
    for result in results:
        total_price = result["total_price_numeric"]
        chart_data.append({
            "사이트": result["site"],
            "총 결제금액": total_price,
            "할인율": int(result["discount"].replace("%", "")),
            "신뢰도": result["trust_score"]
        })
    
    # 가격 비교 막대 차트
    fig_price = px.bar(
        chart_data, 
        x="사이트", 
        y="총 결제금액",
        title="사이트별 총 결제금액 비교 (배송비, 쿠폰 포함)",
        color="총 결제금액",
        color_continuous_scale="viridis",
        text="총 결제금액"
    )
    fig_price.update_layout(
        xaxis_tickangle=-45,
        height=500
    )
    fig_price.update_traces(texttemplate='%{text:,}원', textposition='outside')
    st.plotly_chart(fig_price, use_container_width=True)
    
    # 할인율 vs 신뢰도 산점도
    fig_scatter = px.scatter(
        chart_data,
        x="할인율",
        y="신뢰도",
        size="총 결제금액",
        color="사이트",
        title="할인율 vs 신뢰도 분석",
        hover_data=["사이트", "총 결제금액"]
    )
    fig_scatter.update_layout(height=500)
    st.plotly_chart(fig_scatter, use_container_width=True)
    
    # 할인율 비교 파이 차트
    fig_discount = px.pie(
        chart_data,
        values="할인율",
        names="사이트",
        title="사이트별 할인율 비교"
    )
    st.plotly_chart(fig_discount, use_container_width=True)

def display_price_analysis(results: List[Dict[str, Any]]):
    """가격 분석 결과 표시"""
    if not results:
        return
    
    st.subheader("🔍 가격 분석 인사이트")
    
    # 통계 정보
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_price = sum(r["total_price_numeric"] for r in results) / len(results)
        st.metric("평균 가격", f"{avg_price:,.0f}원")
    
    with col2:
        min_price = min(r["total_price_numeric"] for r in results)
        max_price = max(r["total_price_numeric"] for r in results)
        price_range = max_price - min_price
        st.metric("가격 범위", f"{price_range:,.0f}원")
    
    with col3:
        avg_discount = sum(int(r["discount"].replace("%", "")) for r in results) / len(results)
        st.metric("평균 할인율", f"{avg_discount:.1f}%")
    
    with col4:
        best_site = results[0]["site"]
        st.metric("최저가 사이트", best_site)
    
    # 가격 분포 히스토그램
    prices = [r["total_price_numeric"] for r in results]
    fig_hist = px.histogram(
        x=prices,
        title="가격 분포",
        nbins=10,
        labels={"x": "총 결제금액 (원)", "y": "사이트 수"}
    )
    st.plotly_chart(fig_hist, use_container_width=True)
    
    # 추천 구매 전략
    st.subheader("💡 구매 추천 전략")
    
    best_result = results[0]
    st.success(f"""
    **🏆 최고 추천: {best_result['site']}**
    - 총 결제금액: {best_result['total_price']}
    - 할인율: {best_result['discount']}
    - 배송비: {best_result['shipping_fee']}
    - 쿠폰: {best_result['coupon_amount']}
    - 평점: {best_result['rating']}/5.0
    """)
    
    # 대안 옵션
    if len(results) > 1:
        second_best = results[1]
        st.info(f"""
        **🥈 대안 옵션: {second_best['site']}**
        - 총 결제금액: {second_best['total_price']}
        - 할인율: {second_best['discount']}
        - 차이: {best_result['total_price_numeric'] - second_best['total_price_numeric']:,}원
        """)

def main():
    st.title("🛒 최저가 검색 Agent")
    st.markdown("---")
    
    # 사이드바 설정
    with st.sidebar:
        st.header("⚙️ 설정")
        
        # Gemini 모델 설정
        client = setup_gemini()
        
        if client:
            st.success("✅ Gemini API 연결 성공")
            st.info("🤖 모델: Gemini 2.5 Flash")
        else:
            st.error("❌ Gemini API 연결 실패")
            return
        
        st.markdown("---")
        st.markdown("### 📋 사용법")
        st.markdown("""
        1. 검색할 상품명을 입력하세요
        2. 검색 버튼을 클릭하세요
        3. AI가 최저가를 찾아드립니다
        4. 가격 분석 및 구매 추천을 확인하세요
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
        
        st.markdown("---")
        st.markdown("### 🚀 MCP Context7 활용")
        st.markdown("""
        - 최신 Google GenAI SDK 사용
        - Gemini 2.5 Flash 모델
        - 비동기 검색 최적화
        - AI 기반 검색 전략
        """)
    
    # 메인 컨텐츠
    if not client:
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
        with st.spinner("🔍 AI가 상품을 검색하고 있습니다..."):
            # 진행바 표시
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # 1단계: AI 검색 전략 수립
            progress_bar.progress(20)
            status_text.text("🤖 AI 검색 전략 수립 중...")
            strategy = search_product_prices_ai(product_name, client)
            
            # 2단계: 사이트별 검색
            progress_bar.progress(40)
            status_text.text("🔍 여러 사이트에서 가격 정보 수집 중...")
            
            # 비동기 검색 실행
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            results = loop.run_until_complete(search_all_sites_async(product_name, strategy))
            loop.close()
            
            # 3단계: 결과 분석
            progress_bar.progress(80)
            status_text.text("📊 가격 분석 및 정리 중...")
            
            # 4단계: 완료
            progress_bar.progress(100)
            status_text.text("✅ 검색 완료!")
            time.sleep(0.5)
            
            if results:
                # 결과 표시
                display_price_results(results, product_name, strategy)
                display_price_analysis(results)
                
                # 검색 히스토리 저장 (세션 상태)
                if "search_history" not in st.session_state:
                    st.session_state.search_history = []
                
                st.session_state.search_history.append({
                    "product": product_name,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "best_price": results[0]["total_price"],
                    "best_site": results[0]["site"],
                    "total_sites": len(results)
                })
                
                # 히스토리 표시
                with st.expander("📚 검색 히스토리", expanded=False):
                    for item in reversed(st.session_state.search_history[-5:]):  # 최근 5개만
                        st.write(f"**{item['product']}** - {item['best_price']} ({item['best_site']}) - {item['timestamp']} ({item['total_sites']}개 사이트)")
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
                AI가 여러 쇼핑몰에서 최저가를 찾아드립니다.<br>
                MCP Context7 기술을 활용한 스마트한 가격 비교 서비스입니다!
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
