---
title: "[Deep Dive] useEffect vs useLayoutEffect 실행 타이밍과 브라우저 렌더링"
date: 2026-03-22 08:08:07 +0900
categories: [개발뉴스]
tags: [CS, 심화]
---

## 표면적 이해
React에서 side effect를 처리하는 hook으로 useEffect와 useLayoutEffect가 있으며, 브라우저 렌더링 타이밍에 따라 차이가 있습니다.

## Deep Dive

### 왜 필요한가?
- 이 기술이 해결하는 문제: 컴포넌트가 렌더링되면서 발생하는 side effect를 처리하는 문제입니다. 이전에는 class 컴포넌트에서 componentWillUnmount, componentDidUpdate와 같은 라이프 사이클 메서드를 사용했지만, 함수 컴포넌트에서는 이러한 메서드를 사용할 수 없습니다.
- 이전 방식의 한계: class 컴포넌트의 라이프 사이클 메서드는 함수 컴포넌트에서 사용할 수 없으며, 함수 컴포넌트에서는 side effect를 처리하는 새로운 방법이 필요했습니다.

### 내부 동작 원리
- 핵심 메커니즘 설명: useEffect와 useLayoutEffect는 모두 브라우저 렌더링 후에 실행되는 hook입니다. 그러나 useEffect는 브라우저 렌더링 후에 비동기적으로 실행되며, useLayoutEffect는 동기적으로 실행됩니다.
```
                              +-------------------+
                              |  컴포넌트 렌더링  |
                              +-------------------+
                                        |
                                        |
                                        v
                              +-------------------+
                              |  useLayoutEffect  |
                              |  (동기적 실행)    |
                              +-------------------+
                                        |
                                        |
                                        v
                              +-------------------+
                              |  브라우저 렌더링  |
                              |  (화면에 표시)    |
                              +-------------------+
                                        |
                                        |
                                        v
                              +-------------------+
                              |  useEffect      |
                              |  (비동기적 실행)  |
                              +-------------------+
```

### 코드로 이해하기
```typescript
import { useState, useEffect, useLayoutEffect } from 'react';

function MyComponent() {
  const [count, setCount] = useState(0);

  useEffect(() => {
    console.log('useEffect:', count);
  }, [count]);

  useLayoutEffect(() => {
    console.log('useLayoutEffect:', count);
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
// 잘못된 사용 예: useEffect에서 DOM을 직접 조작하는 경우
useEffect(() => {
  document.getElementById('my-element').style.color = 'red';
}, []);

// 올바른 사용 예: useLayoutEffect에서 DOM을 직접 조작하는 경우
useLayoutEffect(() => {
  document.getElementById('my-element').style.color = 'red';
}, []);
```

### 비교 분석

| 구분 | useEffect | useLayoutEffect |
|------|----------|-----------------|
| 실행 타이밍 | 브라우저 렌더링 후 비동기적 실행 | 브라우저 렌더링 후 동기적 실행 |
| DOM 조작 | 권장하지 않음 | 권장 |
| 성능 | 빠름 | 느림 |

### 실전 팁
- Best Practice: useEffect를 사용할 때는 의존성 배열을 항상 지정하세요. 의존성 배열을 지정하지 않으면, 컴포넌트가 렌더링될 때마다 useEffect가 실행됩니다.
- 흔한 실수와 해결법: useEffect에서 비동기적으로 실행되는 함수를 사용하는 경우, 함수가 컴포넌트가 언마운트된 후에 호출되는 경우를 생각해 보세요. 이 경우, useEffect의 cleanup 함수를 사용하여 함수를할 수 있습니다.
- 성능 관련 주의사항: useEffect와 useLayoutEffect는 브라우저 렌더링 후에 실행되므로, 성능에 큰 영향을 미칩니다. 따라서, 불필요한 side effect를 제거하고, 최적화할 수 있는 부분을 최적화하세요.

### 한 줄 정리
useEffect와 useLayoutEffect는 브라우저 렌더링 타이밍에 따라 다르게 사용되어야 하며, 의존성 배열을 지정하고, cleanup 함수를 사용하여 성능을 최적화할 수 있습니다.