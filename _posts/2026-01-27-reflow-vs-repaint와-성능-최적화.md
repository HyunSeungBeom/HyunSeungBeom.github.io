---
title: "[Deep Dive] Reflow vs Repaint와 성능 최적화"
date: 2026-01-27 23:06:43 +0900
categories: [개발뉴스]
tags: [CS, 심화]
---

## 표면적 이해
Reflow와 Repaint는 웹 브라우저의 렌더링 프로세스에서 중요한 역할을 하는 두 가지 개념으로, 성능 최적화를 위해 이해하는 것이 필요하다.

## Deep Dive

### 왜 필요한가?
- Reflow와 Repaint는 웹 페이지의 레이아웃과 시각적 속성을 업데이트할 때 발생하는 두 가지 별개의 프로세스다. 이전 방식에서는 이러한 프로세스에 대한 이해가 부족하여 성능 문제가 자주 발생했다.

### 내부 동작 원리
- Reflow는 DOM 노드의 레이아웃을 변경할 때 발생하는 프로세스다. 이는 너비, 높이, 폰트 크기 등 레이아웃 관련 속성이 변경되었을 때 발생한다.
- Repaint는 DOM 노드의 시각적 속성을 변경할 때 발생하는 프로세스다. 이는 배경색, 텍스트 색상 등 시각적 속성이 변경되었을 때 발생한다.
 
```
                      +---------------+
                      |  DOM 트리  |
                      +---------------+
                             |
                             |
                             v
                      +---------------+
                      | Reflow(레이아웃) |
                      +---------------+
                             |
                             |
                             v
                      +---------------+
                      | Repaint(렌더링) |
                      +---------------+
                             |
                             |
                             v
                      +---------------+
                      |  화면 업데이트  |
                      +---------------+
```

### 코드로 이해하기

```typescript
// 레이아웃 변경 예: Reflow 발생
const element = document.getElementById('myElement');
element.style.width = '100px'; // Reflow 발생

// 시각적 속성 변경 예: Repaint 발생
const element = document.getElementById('myElement');
element.style.backgroundColor = 'red'; // Repaint 발생
```

```typescript
// 잘못된 사용 예: 불필요한 Reflow 발생
for (let i = 0; i < 100; i++) {
  const element = document.getElementById('myElement');
  element.style.width = i + 'px'; // 매번 Reflow 발생
}

// 올바른 사용 예: Reflow 최소화
const element = document.getElementById('myElement');
element.style.width = '100px'; // 한 번 Reflow 발생
```

### 비교 분석

| 구분 | Reflow | Repaint | Layout 변경 |
|------|---|---|---|
| 설명 | 레이아웃을 변경 | 시각적 속성을 변경 | 너비, 높이 등 레이아웃 속성 변경 |
| 발생 시점 | 레이아웃 변경 시 | 시각적 속성 변경 시 | 레이아웃 변경 시 |
| 성능 영향 | 높은 | 낮은 | 높은 |

### 실전 팁
- 가능하면 Reflow를 최소화하려고 노력해야 한다. 이를 위해 레이아웃 변경을 한 번에 묶어서 수행하는 것이 유용하다.
- DOM 노드를 수정하기 전에 DOM 노드를 문서에서 분리하고, 수정 완료 후에 다시 문서에 붙여 넣는 방법을 사용할 수 있다.
- 성능 관련 주의사항으로는 애니메이션을 수행할 때 레이아웃 변경을 피하는 것이 중요하다.

### 한 줄 정리
Reflow와 Repaint는 웹 브라우저의 렌더링 프로세스에서 각각 레이아웃과 시각적 속성을 업데이트하는 프로세스로, 성능 최적화를 위해 각 프로세스의 특징과 발생 시점을 이해하여 최적화하는 것이 중요하다.