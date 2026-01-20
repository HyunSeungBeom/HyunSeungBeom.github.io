---
title: "[Deep Dive] React Fiber Architecture와 Reconciliation 알고리즘"
date: 2026-01-20 23:06:14 +0900
categories: [개발뉴스]
tags: [CS, 심화]
---

## 표면적 이해
React Fiber Architecture와 Reconciliation 알고리즘은 React가 사용자 인터페이스를 효율적으로 업데이트하고 렌더링할 수 있도록 도와주는 핵심 기술입니다.

## Deep Dive

### 왜 필요한가?
- 이 기술이 해결하는 문제: 이전의 React에서 Virtual DOM을 업데이트 하는 과정에서 전체 트리가 한 번에 업데이트 되면서 성능 이슈가 발생했습니다. Fiber Architecture와 Reconciliation 알고리즘은 이러한 성능 이슈를 해결하기 위해 도입되었습니다.
- 이전 방식의 한계: 이전에 React는 업데이트가 발생할 때마다 전체 Virtual DOM을 재조성하고 비교하는 방식으로 동작했습니다. 그러나 이러한 방식은 큰 규모의 애플리케이션에서 성능 이슈를 발생시켰습니다.

### 내부 동작 원리
- 핵심 메커니즘 설명: Fiber Architecture는 React 컴포넌트 트리를 작은 단위의fiber로 분할하여 관리합니다. Reconciliation 알고리즘은 fiber 트리를 비교하고 업데이트하는 알고리즘입니다.
- ASCII 다이어그램으로 시각화:
```
       +---------------+
       |  ROOT FIBER  |
       +---------------+
             |
             |
             v
       +---------------+
       |  CHILD FIBER  |
       +---------------+
             |
             |
             v
       +---------------+
       |  GRANDCHILD  |
       |  FIBER        |
       +---------------+
```
이 다이어그램은 React의 fiber 트리 구조를 보여줍니다. 각각의 fiber는 부모 자식 관계를 가지며, Reconciliation 알고리즘은 이러한fiber 트리를 비교하고 업데이트합니다.

### 코드로 이해하기
```typescript
import React from 'react';

function App() {
  const [count, setCount] = React.useState(0);

  return (
    <div>
      <p>count: {count}</p>
      <button onClick={() => setCount(count + 1)}>Increase</button>
    </div>
  );
}
```
위의 예제는fiber 트리가 업데이트되는 과정을 보여줍니다. `setCount` 함수가 호출되면 React는 fiber 트리를 업데이트하고 Reconciliation 알고리즘을 사용하여 필요한 변화를 계산합니다.

```typescript
// 잘못된 사용 예 (❌)
// 함수 내부에서 복잡한 연산을 수행하여 fiber 트리가 변경되는 경우
function App() {
  const [count, setCount] = React.useState(0);

  React.useEffect(() => {
    // 복잡한 연산
  }, [count]);

  return (
    <div>
      <p>count: {count}</p>
      <button onClick={() => setCount(count + 1)}>Increase</button>
    </div>
  );
}

// 올바른 사용 예 (✅)
// 함수 외부에서 연산을 수행하고, 결과 값을 state에 저장하는 경우
function App() {
  const [count, setCount] = React.useState(0);

  const handleIncrease = () => {
    // 복잡한 연산
    const newCount = count + 1;
    setCount(newCount);
  };

  return (
    <div>
      <p>count: {count}</p>
      <button onClick={handleIncrease}>Increase</button>
    </div>
  );
}
```
위의 예제는fiber 트리가 업데이트되는 경우에 따른 올바른 사용법을 보여줍니다.

### 비교 분석

| 구분 | fiber 이전 | fiber 이후 | Virtual DOM |
|------|---------|---------|---------|
| 성능 |低       | 高      | 高      |
| 복잡도 | 高      | 低      | 中      |
| 업데이트 방식 | 전체 트리 | 부분 업데이트 | 부분 업데이트 |

### 실전 팁
- Best Practice: fiber 트리를 업데이트할 때는 `useState`와 `useEffect`를 사용하여 상태를 관리하고 사이드 이펙트를 처리합니다.
- 흔한 실수와 해결법: fiber 트리를 업데이트할 때는 상태를 올바르게 관리하고, 사이드 이펙트를 처리하여 성능 이슈를 방지합니다.
- 성능 관련 주의사항: 큰 규모의 애플리케이션에서 fiber 트리를 업데이트할 때는 성능 이슈를 주의하여야 하며, `shouldComponentUpdate`와 `React.memo`를 사용하여 불필요한 업데이트를 방지할 수 있습니다.

### 한 줄 정리
React Fiber Architecture와 Reconciliation 알고리즘은 React의 성능과 효율성을 향상시키는 핵심 기술입니다.