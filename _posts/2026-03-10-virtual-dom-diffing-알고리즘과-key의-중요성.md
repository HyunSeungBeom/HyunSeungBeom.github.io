---
title: "[Deep Dive] Virtual DOM Diffing 알고리즘과 Key의 중요성"
date: 2026-03-10 08:09:01 +0900
categories: [개발뉴스]
tags: [CS, 심화]
---

## 표면적 이해
Virtual DOM Diffing 알고리즘은 Virtual DOM과 실제 DOM의 차이점을 효율적으로 계산하여 업데이트 하는 기술이다.

## Deep Dive

### 왜 필요한가?
- 이 기술이 해결하는 문제: 브라우저의DOM은 동적 콘텐츠의 변경 시마다 브라우저가 DOM을 업데이트하여 렌더링 하는데 이는 많은 비용이 드는 작업이다. Virtual DOM Diffing 알고리즘은 DOM의 변화를 최소화 하여 브라우저의 렌더링 비용을 줄이는 데 필요한 teknik이다.
- 이전 방식의 한계: 이전에는 DOM을 직접 수정하여 업데이트 하는 방식을 사용하였는데, 이러한 방식은 브라우저가 전체 DOM을 다시 렌더링 하여 비용이 많이 드는 문제가 있었다.

### 내부 동작 원리
- 핵심 메커니즘 설명: Virtual DOM Diffing 알고리즘은 두 개의 Virtual DOM 트리(이전 트리와 업데이트 된 트리)를 비교하여 그 차이점을 계산한다. 이 차이점을 통해 실제 DOM을 업데이트하여 렌더링 하는데 필요한 최소의 동작만 수행한다.
- ASCII 다이어그램으로 시각화:
```
        +---------------+
        |  Virtual DOM  |
        +---------------+
                  |
                  |
                  v
        +---------------+
        |  Diffing      |
        |  ()       |
        +---------------+
                  |
                  |
                  v
        +---------------+
        |  실제 DOM     |
        |  (업데이트)   |
        +---------------+
```

### 코드로 이해하기
```typescript
// Virtual DOM Diffing 알고리즘의한 예
interface VNode {
  tag: string;
  children: VNode[];
}

function diff(oldVNode: VNode, newVNode: VNode) {
  // 두 개의 트리를 비교하여 차이점을 계산
  if (oldVNode.tag !== newVNode.tag) {
    // 태그가 변경되었을 경우
    return newVNode;
  }

  // 자식 노드를 비교
  const children = [];
  for (let i = 0; i < newVNode.children.length; i++) {
    children.push(diff(oldVNode.children[i], newVNode.children[i]));
  }

  return { ...oldVNode, children };
}
```

```typescript
// 잘못된 사용 예
// Virtual DOM에 불필요한 key 속성을 사용하는 경우
const vNode = {
  tag: 'div',
  children: [
    { tag: 'p', key: Math.random() }, // key가 변경되면 불필요한 재렌더링이 발생
  ],
};

// 올바른 사용 예
const vNode = {
  tag: 'div',
  children: [
    { tag: 'p', key: 'p-1' }, // key가 변경되지 않으면 재렌더링이 되지 않음
  ],
};
```

### 비교 분석
| 구분 | Virtual DOM | 실제 DOM | Reconciliation |
|------|------------|----------|---------------|
| 렌더링 비용 |       | 높은      | 최소화         |
| 업데이트 속도 | 빠른        | 느린      | 빠른           |
| DOM의 변동 | 최소화      | 최대화    | 최소화         |

### 실전 팁
- Best Practice: Virtual DOM에 key 속성을 지정하여 불필요한 재렌더링을 피하라.
- 흔한 실수와 해결법: 불필요한 key 속성 사용은 재렌더링을 발생시키므로 주의하라.
- 성능 관련 주의사항: Virtual DOM의 크기가 너무 클 경우 성능에 영향을 미칠 수 있으므로 최적화가 필요하다.

### 한 줄 정리
Virtual DOM Diffing 알고리즘은 Virtual DOM과 실제 DOM의 차이점을 효율적으로 계산하여 업데이트 하는 기술로 성능을 향상시키는데 중요한 역할을 한다.