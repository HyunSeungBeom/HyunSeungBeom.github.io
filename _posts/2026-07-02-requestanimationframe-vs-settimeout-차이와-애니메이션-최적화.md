---
title: "[Deep Dive] requestAnimationFrame vs setTimeout 차이와 애니메이션 최적화"
date: 2026-07-02 08:32:17 +0900
categories: [개발뉴스]
tags: [CS, 심화]
---

## 표면적 이해
requestAnimationFrame과 setTimeout의 차이점을 고 애니메이션을 최적화하는 방법을 탐구합니다.

## Deep Dive

### 왜 필요한가?
- 애니메이션과 그래픽 처리를 할 때 프레임률을 유지하는 것이 중요합니다. 이전 방식에서는 setTimeout을 사용하여 애니메이션을 구현했습니다. 그러나 setTimeout은 시스템의 부하와 렌더링 주기에 따라 예측할 수 없는 지연을 일으킵니다. 따라서 requestAnimationFrame이 등장했습니다.

### 내부 동작 원리
- requestAnimationFrame은 브라우저의 렌더링 주기에 따라 호출됩니다. 브라우저는 60FPS를 목표로 렌더링을 수행하며, requestAnimationFrame 함수는 이 렌더링 주기에 맞추어 호출됩니다. 아래의 ASCII 다이어그램은 이 과정을 나타냅니다.
```
+---------------+
|  브라우저   |
+---------------+
       |
       |  렌더링 주기
       v
+---------------+
| requestAnimationFrame |
|  (콜백 함수 호출)    |
+---------------+
       |
       |  애니메이션 처리
       v
+---------------+
|  브라우저 렌더링  |
+---------------+
```

### 코드로 이해하기
```typescript
// 애니메이션 함수
function animate() {
  // 애니메이션 처리
  console.log('애니메이션 처리');
  requestAnimationFrame(animate); // 다음 렌더링 주기 호출
}

// setTimeout의 잘못된 사용 예
// setInterval(() => {
//   console.log('setTimeout의 잘못된 사용');
// }, 1000 / 60); // 60FPS를 목표로 하지만 실제로는 변동이 큼

// requestAnimationFrame의 올바른 사용 예
requestAnimationFrame(animate);
```

### 비교 분석

| 구분 | setTimeout | requestAnimationFrame |
|------|------------|----------------------|
| 호출 주기 | 고정된 시간 간격 | 브라우저의 렌더링 주기 |
| 성능 | 예측할 수 없는 지연 | 60FPS를 유지하여 부드러운 애니메이션 |
| 브라우저의 렌더링 주기 고려 | X | O |

### 실전 팁
- requestAnimationFrame을 사용하여 애니메이션을 구현할 때, 중첩된 호출을 피하여 성능 최적화를 해야 합니다. 이는 애니메이션의 부드러움을 유지하면서도 불필요한 계산을 줄일 수 있습니다.
- setTimeout을 사용하는 경우, 예를 들어 60FPS를 유지하려고 할 때 실제로 60FPS를 manten할 수 없다는 것을 명심하세요. requestAnimationFrame을 사용하여 브라우저의 렌더링 주기와 일치시키는 것이 더 효율적입니다.

### 한 줄 정리
requestAnimationFrame은 브라우저의 렌더링 주기에 따라 호출되는 함수로, 부드러운 애니메이션과 그래픽 처리를 가능하게 해줍니다.