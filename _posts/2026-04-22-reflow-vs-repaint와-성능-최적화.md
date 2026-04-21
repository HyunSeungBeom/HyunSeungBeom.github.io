---
title: "[Deep Dive] Reflow vs Repaint와 성능 최적화"
date: 2026-04-22 08:16:32 +0900
categories: [개발뉴스]
tags: [CS, 심화]
---

## 표면적 이해
리액트의 렌더링 최적화를 위한 Reflow와 Repaint의 차이점을 이해하는 것

## Deep Dive

### 왜 필요한가?
- Reflow와 Repaint는 브라우저의 렌더링 과정을 최적화하기 위한 두 가지 주요 기법입니다. 이전 방식의 한계는 렌더링 프로세스가 매번 발생하여 성능을 저하하는 것이었으며, 이를 최적화하기 위해 리액트는 Virtual DOM을 도입하여 변경 사항을 효율적으로 관리합니다.

### 내부 동작 원리
- Reflow는 레이아웃이 변경될 때 발생하며, 전체 문서의 레이아웃을 재계산합니다. 반면에 Repaint는 요소의 스타일이 변경되었을 때 발생하며, 화면에 다시 그립니다. 리액트의 렌더링 과정은 다음과 같이 표현할 수 있습니다:
```
                      +---------------+
                      |  리액트 컴포넌트  |
                      +---------------+
                             |
                             |
                             v
                      +---------------+
                      |  Virtual DOM  |
                      +---------------+
                             |
                             |
                             v
                      +---------------+
                      |  Reconciliation  |
                      +---------------+
                             |
                             |
                             v
                      +---------------+
                      |  DOM 변경 사항  |
                      +---------------+
                             |
                             |
                             v
                      +---------------+
                      |  Reflow/Repaint  |
                      +---------------+
```

### 코드로 이해하기

```typescript
import React, { useState, useEffect } from 'react';

function Counter() {
  const [count, setCount] = useState(0);

  useEffect(() => {
    document.title = `Count: ${count}`;
  }, [count]);

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>Increment</button>
    </div>
  );
}
```

```typescript
// 잘못된 사용 예: 매번 렌더링 시 DOM을 변경
function WrongCounter() {
  const [count, setCount] = useState(0);

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>Increment</button>
      {Array.from({ length: 1000 }, (_, i) => (
        <div key={i}>{i}</div>
      ))}
    </div>
  );
}

// 올바른 사용 예: 불필요한 렌더링을 피하기 위해 메모이제이션 사용
function CorrectCounter() {
  const [count, setCount] = useState(0);
  const memoizedItems = React.useMemo(() => Array.from({ length: 1000 }, (_, i) => (
    <div key={i}>{i}</div>
  )), []);

  return (
    <div>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>Increment</button>
      {memoizedItems}
    </div>
  );
}
```

### 비교 분석

| 구분 | Reflow | Repaint |
|------|---|---|
| 발생 시점 | 레이아웃 변경 시 | 스타일 변경 시 |
| 영향 | 전체 문서 레이아웃 재계산 | 화면에 다시 그리기 |
| 성능 영향 | 큰 영향을 미침 | 상대적으로 작은 영향을 미침 |

### 실전 팁
- 불필요한 렌더링을 피하기 위해 shouldComponentUpdate 사용
- 메모이제이션을 사용하여 변경 사항을 최적화
- 큰DOM 변경이 필요한 경우, 배치 업데이트 사용
- 성능 관련 주의사항: 렌더링 과정에서 DOM 변경을 최소화하기

### 한 줄 정리
리액트의 렌더링 최적화를 위해서는 Reflow와 Repaint의 차이점을 이해하고, 불필요한 렌더링을 피하기 위해 메모이제이션과 배치 업데이트를 사용해야 합니다.