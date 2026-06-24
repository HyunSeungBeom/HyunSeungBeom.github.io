---
title: "[Deep Dive] React Server Components vs Client Components 아키텍처"
date: 2026-06-25 08:28:36 +0900
categories: [개발뉴스]
tags: [CS, 심화]
---

## 표면적 이해
React Server Components와 Client Components 아키텍처는 웹 애플리케이션을 구축하는 데 사용하는 두 가지 주요 아키텍처이다.

## Deep Dive

### 왜 필요한가?
이 기술은 웹 애플리케이션 개발에서 서버와 클라이언트 사이의 데이터 교환 및 렌더링 효율성을 높이는 데 사용된다. 이전 방식의 한계는 서버에서 데이터를 처리하고 클라이언트에서 렌더링하는 데 시간과 리소스가 많이 소요되는 것이었다.

### 내부 동작 원리
React Server Components는 서버에서 컴포넌트를 렌더링하고, Client Components는 클라이언트에서 컴포넌트를 렌더링한다. ASCII 다이어그램으로 시각화하면 다음과 같다.
```
          +---------------+
          |  Server     |
          +---------------+
                  |
                  |  요청
                  v
          +---------------+
          |  React Server  |
          |  Components     |
          +---------------+
                  |
                  |  렌더링
                  v
          +---------------+
          |  HTML         |
          +---------------+
                  |
                  |  응답
                  v
          +---------------+
          |  Client     |
          +---------------+
                  |
                  |  요청
                  v
          +---------------+
          |  React Client  |
          |  Components     |
          +---------------+
                  |
                  |  렌더링
                  v
          +---------------+
          |  UI         |
          +---------------+
```

### 코드로 이해하기
다음은 React Server Components와 Client Components의 예제 코드이다.
```typescript
// React Server Components 예제
import { useState } from 'react';

interface ServerComponentProps {
  name: string;
}

const ServerComponent: React.FC<ServerComponentProps> = ({ name }) => {
  const [count, setCount] = useState(0);

  return (
    <div>
      <h1>{name}</h1>
      <p>카운트: {count}</p>
      <button onClick={() => setCount(count + 1)}>증가</button>
    </div>
  );
};

export default ServerComponent;
```

```typescript
// React Client Components 예제
import { useState, useEffect } from 'react';

interface ClientComponentProps {
  name: string;
}

const ClientComponent: React.FC<ClientComponentProps> = ({ name }) => {
  const [count, setCount] = useState(0);

  useEffect(() => {
    // 클라이언트에서 데이터를 가져옴
    const fetchData = async () => {
      const response = await fetch('/api/data');
      const data = await response.json();
      setCount(data.count);
    };
    fetchData();
  }, []);

  return (
    <div>
      <h1>{name}</h1>
      <p>카운트: {count}</p>
      <button onClick={() => setCount(count + 1)}>증가</button>
    </div>
  );
};

export default ClientComponent;
```

### 비교 분석
다음은 React Server Components와 Client Components의 비교 분석이다.
| 구분 | React Server Components | React Client Components |
|------|-------------------------|-------------------------|
| 렌더링 | 서버에서 렌더링 | 클라이언트에서 렌더링 |
| 데이터 처리 | 서버에서 데이터 처리 | 클라이언트에서 데이터 처리 |
| 성능 | 빠른 렌더링 및 데이터 처리 | 느린 렌더링 및 데이터 처리 |

### 실전 팁
- React Server Components를 사용할 때는 서버의 성능을 고려해야 한다.
- Client Components를 사용할 때는 클라이언트의 성능을 고려해야 한다.
- 데이터를 처리할 때는 캐시를 사용하여 성능을 verbessern할 수 있다.

### 한 줄 정리
React Server Components와 Client Components는 웹 애플리케이션 개발에서 사용하는 두 가지 주요 아키텍처이다.