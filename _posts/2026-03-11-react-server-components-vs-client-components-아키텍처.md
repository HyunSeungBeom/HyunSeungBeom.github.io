---
title: "[Deep Dive] React Server Components vs Client Components 아키텍처"
date: 2026-03-11 08:09:00 +0900
categories: [개발뉴스]
tags: [CS, 심화]
---

## 표면적 이해
React Server Components vs Client Components 아키텍처는 서버와 클라이언트에서 실행되는 컴포넌트를 나누어 Rendering 성능을 최적화하는-react의 아키텍처입니다.

## Deep Dive

### 왜 필요한가?
React Server Components와 Client Components를 구분하는 이유는 Rendering 성능을 최적화하기 위해서입니다. 렌더링 성능은 사용자 경험에게 영향을 미치며, 잘못된 아키텍처는 느린 페이지 로딩 시간과 반응성이 저하된 사용자 인터페이스로 이어질 수 있습니다. 이전 방식에서는 클라이언트 사이드 렌더링만을 사용했지만, 이 방법은 초기 로딩 시간이 길고, 동적으로 변경되는 컨텐츠를 렌더링할 때 부드럽지 않을 수 있다는 한계를 가지고 있습니다.

### 내부 동작 원리
React Server Components와 Client Components는 다음과 같은 내부 동작 원리를 가지고 있습니다.
```
                      +---------------+
                      |  요청      |
                      +---------------+
                             |
                             |
                             v
                      +---------------+
                      |  Server   |
                      |  (Initial  |
                      |   Rendering) |
                      +---------------+
                             |
                             |
                             v
                      +---------------+
                      |  HTML     |
                      |  (초기 렌더링 결과) |
                      +---------------+
                             |
                             |
                             v
                      +---------------+
                      |  Client   |
                      |  (동적 렌더링)  |
                      +---------------+
                             |
                             |
                             v
                      +---------------+
                      |  동적      |
                      |  렌더링 결과  |
                      +---------------+
```
위 다이어그램에서 나타난 것처럼, 서버는 초기 렌더링을 처리하고, 클라이언트는 동적으로되는 컨텐츠를 렌더링합니다.

### 코드로 이해하기
```typescript
// Server Components 예
import { useState } from 'react';

const ServerComponent = () => {
  const [count, setCount] = useState(0);

  return (
    <div>
      <p>서버에서 렌더링된 컴포넌트</p>
      <button onClick={() => setCount(count + 1)}>카운트 증가</button>
      <p>카운트: {count}</p>
    </div>
  );
};

// Client Components 예
import { useState, useEffect } from 'react';

const ClientComponent = () => {
  const [data, setData] = useState(null);

  useEffect(() => {
    // 데이터를 불러옵니다.
    const fetchData = async () => {
      const response = await fetch('https://example.com/data');
      const data = await response.json();
      setData(data);
    };
    fetchData();
  }, []);

  if (!data) return <div>로딩 중...</div>;

  return (
    <div>
      <p>클라이언트에서 렌더링된 컴포넌트</p>
      <p>데이터: {data}</p>
    </div>
  );
};
```

```typescript
// 잘못된 사용 예: 서버에서 렌더링하도록 설계된 컴포넌트에서 side-effect를 발생시키는 코드
const WrongServerComponent = () => {
  const [count, setCount] = useState(0);

  // 서버에서 렌더링하도록 설계된 컴포넌트에서 side-effect를 발생시키는 코드
  useEffect(() => {
    // 이 코드는 서버에서 실행되면 안 됩니다.
    const timer = setInterval(() => {
      setCount(count + 1);
    }, 1000);
    return () => clearInterval(timer);
  }, [count]);

  return (
    <div>
      <p>서버에서 렌더링된 컴포넌트</p>
      <p>카운트: {count}</p>
    </div>
  );
};
```

```typescript
// 올바른 사용 예: 서버에서 렌더링하도록 설계된 컴포넌트
const CorrectServerComponent = () => {
  const [count, setCount] = useState(0);

  return (
    <div>
      <p>서버에서 렌더링된 컴포넌트</p>
      <button onClick={() => setCount(count + 1)}>카운트 증가</button>
      <p>카운트: {count}</p>
    </div>
  );
};
```

### 비교 분석

| 구분 | Server Components | Client Components |
|------|------------------|-------------------|
| 렌더링 위치 | 서버 | 클라이언트 |
| 렌더링 시점 | 요청 시 | 요청 후 |
| 사용 목적 | 초기 렌더링 | 동적 렌더링 |
| 특징 | SEO 향상, 초기 로딩 시간 단축 | 사용자 상호작용, 동적 컨텐츠 렌더링 |

### 실전 팁
- Server Components와 Client Components를 분리하여 각각의 컴포넌트가 자신의 역할에 집중할 수 있도록 설계해야 합니다.
- Server Components에서 side-effect를 발생시키는 코드를 피해야 합니다.
- Client Components에서 데이터를 불러올 때는 로딩 상태를 표시할 수 있도록 설계해야 합니다.
- 성능을 최적화하기 위해 렌더링을 최소화하고, 불필요한 재렌더링을 피해야 합니다.

### 한 줄 정리
React Server Components와 Client Components를 분리하여 사용하면 초기 렌더링 성능을 최적화하고, 동적인 컨텐츠를 렌더링할 수 있습니다.