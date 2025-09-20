import React, { useState, useEffect } from 'react';

// 뉴스 기사 데이터 타입을 정의합니다.
interface NewsArticle {
  id: number;
  title: string;
  url: string;
  political_leaning: string;
  created_at: string;
}

const NewsFeed: React.FC = () => {
  // useState에 NewsArticle[] 타입을 지정하여 배열임을 명시합니다.
  const [news, setNews] = useState<NewsArticle[]>([]);

  useEffect(() => {
    fetch('http://localhost:8000/news') // 백엔드 API 주소
      .then(response => response.json())
      .then(data => setNews(data))
      .catch(error => console.error('뉴스 정보를 가져오는 데 실패했습니다:', error));
  }, []); // 빈 배열을 넣어 컴포넌트가 처음 렌더링될 때만 실행되도록 합니다.

  return (
    <div className="news-feed-container">
      <h1>최신 뉴스</h1>
      <div className="news-list">
        {news.length > 0 ? (
          news.map(article => (
            <div key={article.id} className="news-item">
              <h2>{article.title}</h2>
              <a href={article.url} target="_blank" rel="noopener noreferrer">기사 원문 보기</a>
            </div>
          ))
        ) : (
          <p>뉴스 정보를 불러오는 중입니다...</p>
        )}
      </div>
    </div>
  );
};

export default NewsFeed;