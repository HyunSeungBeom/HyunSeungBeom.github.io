---
title: "[Deep Dive] React Fiber Architecture와 Reconciliation"
date: 2026-01-16 10:00:00 +0900
categories: [개발뉴스]
tags: [React, 심화, 면접]
---

## 개요

React 16에서 도입된 **Fiber Architecture**는 React의 핵심 알고리즘을 완전히 재작성한 것입니다. 왜 이런 대규모 변경이 필요했을까요?

기존 Stack Reconciler의 문제:
- 동기적으로 전체 트리를 한 번에 처리
- 작업 중간에 멈출 수 없음
- 긴 작업 시 메인 스레드 블로킹 → UI 버벅임

## 핵심 원리

### Fiber란?

Fiber는 **작업 단위(unit of work)**를 나타내는 JavaScript 객체입니다.

```typescript
interface Fiber {
  type: any;           // 컴포넌트 타입 (함수, 클래스, 'div' 등)
  key: string | null;
  stateNode: any;      // 실제 DOM 노드 또는 클래스 인스턴스
  child: Fiber | null;
  sibling: Fiber | null;
  return: Fiber | null; // 부모 Fiber
  alternate: Fiber | null; // 이전 렌더의 Fiber (Double Buffering)
  effectTag: number;   // 수행할 작업 (Placement, Update, Deletion)
  // ...
}
```

### Double Buffering

React는 두 개의 Fiber 트리를 유지합니다:
- **current**: 현재 화면에 렌더링된 트리
- **workInProgress**: 다음 렌더링을 위해 작업 중인 트리

```
current tree          workInProgress tree
     A        <-->          A'
    / \                    / \
   B   C                  B'  C'
```

### 작업 우선순위 (Lane)

```typescript
const SyncLane = 0b0001;          // 동기 (클릭 등)
const InputContinuousLane = 0b0010; // 연속 입력 (드래그)
const DefaultLane = 0b0100;        // 일반 업데이트
const IdleLane = 0b1000;          // 유휴 시간 작업
```

## Reconciliation 과정

### 1. Render Phase (중단 가능)

```typescript
function workLoopConcurrent() {
  while (workInProgress !== null && !shouldYield()) {
    performUnitOfWork(workInProgress);
  }
}
```

`shouldYield()`로 브라우저에게 제어권을 넘길지 체크합니다.

### 2. Commit Phase (중단 불가)

실제 DOM 변경을 적용하는 단계:
- BeforeMutation: `getSnapshotBeforeUpdate`
- Mutation: DOM 조작
- Layout: `useLayoutEffect`, `componentDidMount`

## 성능 및 트레이드오프

| 방식 | 장점 | 단점 |
|------|------|------|
| Stack (구버전) | 단순, 예측 가능 | UI 블로킹 |
| Fiber (현재) | 부드러운 UX, 우선순위 | 복잡성 증가, 메모리 사용 |

## 면접 Deep Dive

**Q1: Virtual DOM Diffing의 시간복잡도가 O(n)인 이유는?**

A: 일반적인 트리 비교는 O(n³)이지만, React는 두 가지 휴리스틱을 적용합니다:
1. 다른 타입의 요소는 다른 트리를 생성한다고 가정
2. key prop으로 자식 요소의 안정성 힌트 제공

**Q2: useTransition과 useDeferredValue의 차이는?**

A:
- `useTransition`: 상태 업데이트 자체를 낮은 우선순위로 표시
- `useDeferredValue`: 값의 "지연된 버전"을 반환, 긴급한 업데이트가 끝난 후 갱신

**Q3: Concurrent Mode에서 발생할 수 있는 문제는?**

A: Render Phase가 여러 번 실행될 수 있어서:
- 부수 효과가 있는 코드가 여러 번 실행될 수 있음
- `useEffect` 대신 render 중 API 호출하면 문제 발생
- StrictMode에서 의도적으로 두 번 렌더링하는 이유

## 실무 적용 팁

```tsx
// Bad: 모든 상태 업데이트가 동일한 우선순위
const handleClick = () => {
  setSearchQuery(input);  // 긴급
  setSearchResults(fetch(...));  // 덜 긴급
};

// Good: 우선순위 분리
const handleClick = () => {
  setSearchQuery(input);  // 긴급
  startTransition(() => {
    setSearchResults(fetch(...));  // 낮은 우선순위
  });
};
```

흔한 실수:
- key로 index 사용 → 리스트 변경 시 불필요한 리렌더
- 불필요한 리렌더 최적화에 집착 → React가 이미 충분히 빠름
