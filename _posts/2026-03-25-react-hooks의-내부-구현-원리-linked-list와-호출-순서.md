---
title: "[Deep Dive] React Hooks의 내부 구현 원리 (Linked List와 호출 순서)"
date: 2026-03-25 08:10:37 +0900
categories: [개발뉴스]
tags: [CS, 심화]
---

## 표면적 이해
React Hooks는 함수형 컴포넌트에서 상태 관리와 부수 효과를 처리하는 방법을 제공한다.

## Deep Dive

### 왜 필요한가?
- 이전에는 함수형 컴포넌트에서 상태를 관리하거나 부수 효과를 처리하기가 어려웠다. 클래스 컴포넌트를 사용하거나 Higher-Order Component를 이용해야 했으며, 이는 코드를 복잡하게 만들었다.
- 이러한 한계를 극복하기 위해 React Hooks가 도입되었다.

### 내부 동작 원리
- React Hooks는 내부적으로 Linked List를 사용하여 Hooks를 관리한다. 각 Hooks는 리스트에 추가되며, 호출서는 이 리스트를 따라서 결정된다.
```
+---------------+
|      Hook1    |
+---------------+
       |
       |
       v
+---------------+
|      Hook2    |
+---------------+
       |
       |
       v
+---------------+
|      Hook3    |
+---------------+
```
- 위 다이어그램에서 각 Hook는 이전 Hook를 참조하며, 이 리스트를 통해 React는 Hooks의 호출 순서를 관리한다.

### 코드로 이해하기

```typescript
import { useState, useEffect } from 'react';

function Example() {
  const [count, setCount] = useState(0);

  useEffect(() => {
    document.title = `You clicked ${count} times`;
  }, [count]);

  return (
    <div>
      <p>You clicked {count} times</p>
      <button onClick={() => setCount(count + 1)}>
        Click me
      </button>
    </div>
  );
}
```

```typescript
// 잘못된 사용 예: Hook을 조건문 안에서 사용
if (true) {
  const [count, setCount] = useState(0); // 이 코드는 Error를 발생시킨다.
}

// 올바른 사용 예: Hook을 함수 최상단에서 사용
function Example() {
  const [count, setCount] = useState(0); // 이 코드는 정상 작동한다.
  if (true) {
    // ...
  }
}
```

### 비교 분석

| 구분 | Function Component | Class Component |
|------|-------------------|----------------|
| 상태 관리 | useState | this.state |
| 부수 효과 | useEffect | componentDidMount, componentDidUpdate |
| 렌더링 | 함수 호출 | render 메서드 호출 |

### 실전 팁
- Hook을 사용할 때 함수 최상단에서 사용해야 한다. 조건문이나 반복문 안에서 사용하면 안된다.
- Hook을 사용할 때는 의존성 배열을 주의해서 관리해야 한다. 의존성 배열이 변경되면 Hook이 재실행된다.
- 성능 관련 주의사항으로는 불필요한 재렌더링을 피하는 것이 중요하다. useMemo, useCallback 등으로 최적화를 할 수 있다.

### 한 줄 정리
React Hooks는 함수형 컴포넌트에서 상태 관리와 부수 효과를 처리하는 데 사용되는 내부적으로 Linked List를 이용한 강력한 도구이다.