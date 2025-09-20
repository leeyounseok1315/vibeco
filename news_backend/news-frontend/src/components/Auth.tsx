import React, { useState } from 'react';

const Auth = () => {
  const [isLogin, setIsLogin] = useState(true);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [politicalAffiliation, setPoliticalAffiliation] = useState('');
  const [error, setError] = useState('');
  const [message, setMessage] = useState('');

  const toggleAuthMode = () => {
    setIsLogin(!isLogin);
    setError('');
    setMessage('');
  };

  const handlePoliticalAffiliation = (affiliation: string) => {
    setPoliticalAffiliation(prev => prev === affiliation ? '' : affiliation);
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setError('');
    setMessage('');

    if (isLogin) {
      // 로그인 로직
      try {
        const response = await fetch('http://localhost:8000/users/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ username, password }),
        });

        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.detail || '로그인에 실패했습니다.');
        }

        setMessage(`환영합니다, ${username}!`);
        // TODO: 로그인 성공 후 토큰 저장 및 페이지 이동 로직 추가
        
      } catch (err: any) {
        setError(err.message);
      }
    } else {
      // 회원가입 로직
      if (password !== confirmPassword) {
        setError('비밀번호가 일치하지 않습니다.');
        return;
      }
      if (!politicalAffiliation) {
        setError('정치 성향을 선택해주세요.');
        return;
      }

      try {
        const response = await fetch('http://localhost:8000/users/register', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            username,
            password,
            political_leaning: politicalAffiliation,
          }),
        });

        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.detail || '회원가입에 실패했습니다.');
        }

        setMessage('회원가입에 성공했습니다! 이제 로그인해주세요.');
        setIsLogin(true); // 로그인 모드로 전환

      } catch (err: any) {
        setError(err.message);
      }
    }
  };

  return (
    <div style={{ display: 'flex', justifyContent: 'center', padding: '2rem' }}>
      <div style={{ width: '100%', maxWidth: '400px' }}>
        <h2>{isLogin ? '로그인' : '회원가입'}</h2>
        <form onSubmit={handleSubmit}>
          {error && <p style={{ color: 'red' }}>{error}</p>}
          {message && <p style={{ color: 'green' }}>{message}</p>}
          <div style={{ marginBottom: '1rem' }}>
            <label htmlFor="username" style={{ display: 'block', marginBottom: '0.5rem' }}>사용자 이름</label>
            <input
              type="text"
              id="username"
              name="username"
              required
              style={{ width: '100%', padding: '0.5rem' }}
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
          </div>
          <div style={{ marginBottom: '1rem' }}>
            <label htmlFor="password" style={{ display: 'block', marginBottom: '0.5rem' }}>비밀번호</label>
            <input
              type="password"
              id="password"
              name="password"
              required
              style={{ width: '100%', padding: '0.5rem' }}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>
          {!isLogin && (
            <>
              <div style={{ marginBottom: '1rem' }}>
                <label htmlFor="confirmPassword" style={{ display: 'block', marginBottom: '0.5rem' }}>비밀번호 확인</label>
                <input
                  type="password"
                  id="confirmPassword"
                  name="confirmPassword"
                  required
                  style={{ width: '100%', padding: '0.5rem' }}
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                />
              </div>
              <div style={{ marginBottom: '1rem' }}>
                <label style={{ display: 'block', marginBottom: '0.5rem' }}>정치 성향</label>
                <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                  <button
                    type="button"
                    onClick={() => handlePoliticalAffiliation('conservative')}
                    style={{
                      width: '30%',
                      padding: '0.5rem',
                      backgroundColor: politicalAffiliation === 'conservative' ? '#007bff' : 'white',
                      color: politicalAffiliation === 'conservative' ? 'white' : 'black',
                      border: '1px solid #ccc',
                    }}
                  >
                    보수
                  </button>
                  <button
                    type="button"
                    onClick={() => handlePoliticalAffiliation('progressive')}
                    style={{
                      width: '30%',
                      padding: '0.5rem',
                      backgroundColor: politicalAffiliation === 'progressive' ? '#007bff' : 'white',
                      color: politicalAffiliation === 'progressive' ? 'white' : 'black',
                      border: '1px solid #ccc',
                    }}
                  >
                    진보
                  </button>
                  <button
                    type="button"
                    onClick={() => handlePoliticalAffiliation('neutral')}
                    style={{
                      width: '30%',
                      padding: '0.5rem',
                      backgroundColor: politicalAffiliation === 'neutral' ? '#007bff' : 'white',
                      color: politicalAffiliation === 'neutral' ? 'white' : 'black',
                      border: '1px solid #ccc',
                    }}
                  >
                    중립
                  </button>
                </div>
              </div>
            </>
          )}
          <button type="submit" style={{ width: '100%', padding: '0.75rem', backgroundColor: '#007bff', color: 'white', border: 'none', cursor: 'pointer' }}>
            {isLogin ? '로그인' : '회원가입'}
          </button>
        </form>
        <button onClick={toggleAuthMode} style={{ background: 'none', border: 'none', color: '#007bff', cursor: 'pointer', marginTop: '1rem', padding: 0 }}>
          {isLogin ? '계정이 없으신가요? 회원가입' : '이미 계정이 있으신가요? 로그인'}
        </button>
      </div>
    </div>
  );
};

export default Auth;