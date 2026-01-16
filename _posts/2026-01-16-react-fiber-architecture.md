---
title: "[Deep Dive] React Fiber Architecture와 Reconciliation"
date: 2026-01-16 10:00:00 +0900
categories: [개발뉴스]
tags: [React, 심화]
---

## TL;DR

React Fiber는 렌더링 작업을 작은 단위로 쪼개서 중단/재개할 수 있게 만든 아키텍처로, UI 블로킹 없이 부드러운 사용자 경험을 제공한다.

## 선행 지식

- React 기본 개념 (컴포넌트, state, props)
- Virtual DOM이 무엇인지
- JavaScript 이벤트 루프 기초

## 탄생 배경

React 15까지는 **Stack Reconciler**를 사용했다. 이름 그대로 콜 스택 기반으로 동작했는데, 치명적인 문제가 있었다.

**문제점:**
- 컴포넌트 트리가 크면 렌더링에 수백 ms 소요
- 렌더링 중간에 멈출 수 없음 (동기적 처리)
- 그동안 메인 스레드 블로킹 → 입력 지연, 애니메이션 끊김

예를 들어, 1000개의 아이템을 렌더링하면 그 작업이 끝날 때까지 사용자의 클릭, 타이핑에 반응할 수 없었다.

## 역사와 발전 과정

| 시점 | 내용 |
|------|------|
| 2016 | Facebook의 Sebastian Markbage가 Fiber 설계 시작 |
| 2017.09 | React 16 출시, Fiber 아키텍처 도입 |
| 2019 | Concurrent Mode 실험적 도입 |
| 2022 | React 18에서 Concurrent Features 정식 출시 |

Sebastian Markbage는 "렌더링 작업을 requestIdleCallback처럼 브라우저의 여유 시간에 조금씩 처리하면 어떨까?"라는 아이디어에서 출발했다.

## 개념 정의

**Fiber**는 두 가지 의미를 가진다:

1. **아키텍처**: React의 새로운 재조정(Reconciliation) 엔진
2. **데이터 구조**: 컴포넌트 인스턴스와 작업 정보를 담는 JavaScript 객체

```typescript
interface Fiber {
  type: any;              // 'div', MyComponent 등
  key: string | null;
  stateNode: any;         // 실제 DOM 노드
  child: Fiber | null;    // 첫 번째 자식
  sibling: Fiber | null;  // 다음 형제
  return: Fiber | null;   // 부모
  alternate: Fiber | null; // 이전 렌더의 Fiber
  flags: number;          // 수행할 작업 플래그
}
```

## 동작 원리

### 1. Double Buffering

React는 두 개의 Fiber 트리를 유지한다:

```
current (화면에 보이는 것)    workInProgress (작업 중)
        App                          App'
       /   \                        /   \
   Header  Main      <--->     Header'  Main'
             |                          |
           List                       List'
```

작업이 완료되면 포인터만 교체하여 workInProgress가 current가 된다.

### 2. 작업 우선순위

```typescript
// Lane 우선순위 (숫자가 작을수록 높음)
SyncLane           // 클릭, 입력 등 즉시 반응 필요
InputContinuousLane // 드래그
DefaultLane        // 일반 setState
IdleLane           // 백그라운드 작업
```

### 3. 렌더 단계 분리

**Render Phase** (중단 가능):
```typescript
function workLoopConcurrent() {
  while (workInProgress !== null && !shouldYield()) {
    performUnitOfWork(workInProgress);
  }
}
```

**Commit Phase** (중단 불가):
- 실제 DOM 조작
- useLayoutEffect 실행

## 실무 활용

### useTransition으로 우선순위 분리

```tsx
function SearchPage() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [isPending, startTransition] = useTransition();

  const handleChange = (e) => {
    // 입력은 즉시 반영 (높은 우선순위)
    setQuery(e.target.value);

    // 검색 결과는 여유있을 때 (낮은 우선순위)
    startTransition(() => {
      setResults(searchItems(e.target.value));
    });
  };

  return (
    <>
      <input value={query} onChange={handleChange} />
      {isPending ? <Spinner /> : <ResultList items={results} />}
    </>
  );
}
```

## 비교 분석

| 항목 | Stack Reconciler (v15) | Fiber (v16+) |
|------|------------------------|--------------|
| 작업 단위 | 전체 트리 | 개별 Fiber |
| 중단 가능 | 불가능 | 가능 |
| 우선순위 | 없음 | Lane 시스템 |
| 애니메이션 | 버벅임 | 부드러움 |
| 메모리 | 적음 | 약간 증가 |
| 복잡도 | 단순 | 복잡 |

## 한계와 주의점

**흔한 실수:**

```tsx
// Bad: render 중 부수 효과
function Component() {
  fetchData(); // Concurrent Mode에서 여러 번 호출될 수 있음
  return <div>...</div>;
}

// Good: useEffect 사용
function Component() {
  useEffect(() => {
    fetchData();
  }, []);
  return <div>...</div>;
}
```

**주의점:**
- Render Phase는 여러 번 실행될 수 있다
- 순수하지 않은 렌더링 로직은 버그 유발
- StrictMode가 두 번 렌더링하는 이유가 이것

## 미래 전망

- **React Compiler (React Forget)**: 자동 메모이제이션으로 수동 최적화 불필요
- **Server Components**: 서버에서 렌더링하여 번들 사이즈 감소
- **Offscreen API**: 숨겨진 컴포넌트 사전 렌더링

## 정리

- Fiber는 렌더링을 작은 단위로 쪼개 중단/재개 가능하게 만든 아키텍처
- Double Buffering과 Lane 시스템으로 우선순위 기반 렌더링
- useTransition, useDeferredValue로 실무에서 활용
- Render Phase의 순수성을 지키는 것이 중요

**결론:** Fiber를 이해하면 React의 성능 최적화가 왜 그렇게 동작하는지 본질적으로 이해할 수 있다.
