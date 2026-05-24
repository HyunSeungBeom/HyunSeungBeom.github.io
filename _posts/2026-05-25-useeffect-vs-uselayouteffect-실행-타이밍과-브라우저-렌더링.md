---
title: "[Deep Dive] useEffect vs useLayoutEffect 실행 타이밍과 브라우저 렌더링"
date: 2026-05-25 08:24:42 +0900
categories: [개발뉴스]
tags: [CS, 심화]
---

## 표면적 이해
useEffect와 useLayoutEffect는 리액트의 두 가지 중요한 hooks로, 서로 다른 실행 타이밍과 브라우저 렌더링에 영향을 미친다.

## Deep Dive

### 왜 필요한가?
- 이 기술들이 해결하는 문제는 브라우저 렌더링과 관련된 사이드 이펙트를 관리하는 것이다. 이전 방식의 한계는 브라우저 렌더링에 대한 명시적 제어가 불가능하고, 렌더링 사이클을 이해하지 못하면 많은 문제가 발생할 수 있다.

### 내부 동작 원리
- 핵심 메커니즘은 브라우저의 렌더링 사이클을 이해하는 것이다. 다음과 같은 ASCII 다이어그램으로 시각화할 수 있다.

```
                     +---------------+
                     |  렌더링 시작  |
                     +---------------+
                             |
                             |
                             v
                     +---------------+
                     |   레이아웃 계산  |
                     +---------------+
                             |
                             |
                             v
                     +---------------+
                     |  useLayoutEffect  |
                     +---------------+
                             |
                             |
                             v
                     +---------------+
                     |   페인트 및 합성  |
                     +---------------+
                             |
                             |
                             v
                     +---------------+
                     |  useEffect      |
                     +---------------+
                             |
                             |
                             v
                     +---------------+
                     |  렌더링 완료    |
                     +---------------+
```

### 코드로 이해하기

```typescript
import { useState, useEffect, useLayoutEffect } from 'react';

function Counter() {
  const [count, setCount] = useState(0);

  useLayoutEffect(() => {
    console.log('useLayoutEffect: 레이아웃 계산 이후 실행');
  }, [count]);

  useEffect(() => {
    console.log('useEffect: 렌더링 완료 이후 실행');
  }, [count]);

  return (
    <div>
      <p>카운트: {count}</p>
      <button onClick={() => setCount(count + 1)}>증가</button>
    </div>
  );
}
```

```typescript
// 잘못된 사용 예
// useLayoutEffect 내에서 DOM을 조작하고 useEffect도 같이 사용하는 경우
useLayoutEffect(() => {
  document.body.style.backgroundColor = 'red';
}, []);
useEffect(() => {
  document.body.style.backgroundColor = 'blue';
}, []);

// 올바른 사용 예
//.useLayoutEffect와 useEffect를 명확하게 구분하여 사용
useLayoutEffect(() => {
  document.body.style.backgroundColor = 'red';
}, []);
useEffect(() => {
  console.log('useEffect: 렌더링 완료 이후 실행');
}, []);
```

### 비교 분석

| 구분 | useEffect | useLayoutEffect |
|------|----------|-----------------|
| 실행 타이밍 | 렌더링 완료 이후 | 레이아웃 계산 이후 |
| 브라우저 렌더링 | 영향을 받지 않음 | 영향을 받을 수 있음 |
| 주로 사용 목적 | 사이드 이펙트 처리 | DOM 관련 처리 |

### 실전 팁
- Best Practice:(useEffect와 useLayoutEffect를 명확하게 구분하여 사용하고, 실행 타이밍을 고려하여 hooks를 사용)
- 흔한 실수와 해결법: DOM을 조작하는 경우 useLayoutEffect를 사용하고, 사이드 이펙트 처리는 useEffect를 사용한다.
- 성능 관련 주의사항: useLayoutEffect는 브라우저 렌더링에 영향을 미칠 수 있으므로 자주 사용하지 않도록 주의한다.

### 한 줄 정리
useEffect와 useLayoutEffect는 서로 다른 실행 타이밍과 브라우저 렌더링에 영향을 미치므로, 명확하게 구분하여 사용해야 한다.