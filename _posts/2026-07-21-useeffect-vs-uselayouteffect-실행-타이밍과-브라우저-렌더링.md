---
title: "[Deep Dive] useEffect vs useLayoutEffect 실행 타이밍과 브라우저 렌더링"
date: 2026-07-21 08:55:51 +0900
categories: [개발뉴스]
tags: [CS, 심화]
---

## 표면적 이해
useEffect와 useLayoutEffect는 두 가지 중요한 hook 함수로, 브라우저 렌더링과 관련된 시점에 코드를 실행시킬 수 있는 기능을 제공한다.

## Deep Dive

### 왜 필요한가?
- React에서 state나 props가 변경되었을 때, 컴포넌트가 갱신되는 과정에서 일부 외부 상태를 갱신하거나, DOM을 변경해야 하는 경우가 있다. 이때 필요한 것이 effect hook이다. 하지만 단순히 effect를 사용할 경우, 브라우저의 렌더링 타이밍과 맞지 않는 코드가 실행될 수 있다. 이전 방식의 한계는 브라우저 렌더링과 DOM을 변경하는 코드를 정확하게 제어할 수 없었다.

### 내부 동작 원리
- React의 Reconciliation과정에서 Virtual DOM을 실제 DOM으로 반영하는 시점에 effect를 실행할 수 있다. Virtual DOM과 실제 DOM을하여 필요한 변경만을 실제 DOM에 반영한다. useLayoutEffect는 브라우저가 렌더링을 마친 직후에 실행되는 반면, useEffect는 브라우저가 렌더링을 마친 후에 브라우저가_idle 상태에 들어간 후에 실행된다.
```
                 +---------------+
                 |  렌더링 시작  |
                 +---------------+
                             |
                             |
                             v
                 +---------------+
                 | Virtual DOM   |
                 |  비교 및 갱신 |
                 +---------------+
                             |
                             |
                             v
                 +---------------+
                 | useLayoutEffect|
                 |  (렌더링 직후) |
                 +---------------+
                             |
                             |
                             v
                 +---------------+
                 |  브라우저_idle |
                 |  상태 확인      |
                 +---------------+
                             |
                             |
                             v
                 +---------------+
                 |  useEffect    |
                 |  (브라우저_idle)|
                 +---------------+
```
### 코드로 이해하기

```typescript
import { useState, useEffect, useLayoutEffect } from 'react';

function MyComponent() {
  const [count, setCount] = useState(0);

  useLayoutEffect(() => {
    console.log('useLayoutEffect 실행');
  }, [count]);

  useEffect(() => {
    console.log('useEffect 실행');
  }, [count]);

  return (
    <div>
      <button onClick={() => setCount(count + 1)}>카운트 증가</button>
      <p>현재 카운트: {count}</p>
    </div>
  );
}
```

```typescript
// 잘못된 사용 예
// useLayoutEffect 안에서 DOM을 변경시키지 말고, DOM을 변경 후 useLayoutEffect를 사용해야 함
useLayoutEffect(() => {
  document.getElementById('myDiv').style.color = 'red';
}, []);
```

```typescript
// 올바른 사용 예
// DOM을 변경 후 useLayoutEffect를 사용해야 함
useEffect(() => {
  document.getElementById('myDiv').style.color = 'red';
}, []);
```

### 비교 분석

| 구분 | useEffect | useLayoutEffect |
|------|---|---|
| 실행 시점 | 브라우저_idle 상태 | 렌더링 직후 |
| 사용 목적 | 부수적인 효과 (외부 상태 갱신 등) | DOM을 변경하거나 layout과 관련된 작업 |
| 예시 | 네트워크 요청, 로깅, 애니메이션 | DOM을 조작하는 코드, 레이아웃에을 주는 코드 |

### 실전 팁
- DOM을 변경하거나 레이아웃에 영향을 미치는 코드는 useLayoutEffect를 사용하고, 부수적인 효과(외부 상태 갱신 등)는 useEffect를 사용한다. 
- useEffect와 useLayoutEffect 내에서 새로운 state를 변경하는 코드는 피해야 한다. 이는 effect의 무한 호출을 유발할 수 있다. 
- 성능 관련 주의사항으로, 불한 effect를 많이 사용한다면 브라우저의 렌더링 성능에 영향을 줄 수 있다.

### 한 줄 정리
useEffect와 useLayoutEffect는 브라우저 렌더링을 고려하여 효과적으로 사용해야 하며, DOM을 변경하거나 레이아웃에 영향을 주는 코드는 useLayoutEffect를, 부수적인 효과는 useEffect를 사용해야 한다.