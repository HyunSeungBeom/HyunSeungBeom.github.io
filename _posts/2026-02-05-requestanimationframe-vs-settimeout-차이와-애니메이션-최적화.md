---
title: "[Deep Dive] requestAnimationFrame vs setTimeout 차이와 애니메이션 최적화"
date: 2026-02-05 08:08:58 +0900
categories: [개발뉴스]
tags: [CS, 심화]
---

## 표면적 이해
requestAnimationFrame과 setTimeout은 애니메이션 구현에 사용되는 두 가지 주요 기술이나, 이들은 성능과 동작 방식에서 차이점을 가지고 있다.

## Deep Dive

### 왜 필요한가?
- 이 기술이 해결하는 문제: 애니메이션의 평도와 성능 최적화를 위해 필요하다. 이전 방식의 한계는 애니메이션 동작이 화면의_refresh_와 싱크되지 않아 애니메이션의 버벅거림이나 지연이 나타날 수 있다.

### 내부 동작 원리
- 핵심 메커니즘 설명: requestAnimationFrame은 브라우저의_refresh_ 주기와 연결되어 동작한다. 따라서 브라우저가 화면을 그리기 직전에 콜백 함수를 호출하여 애니메이션의 다음 프레임을 준비한다. 이와 달리, setTimeout은 지정된 시간 후에 콜백 함수를 호출한다.
```
+---------------+
|  브라우저   |
|  (화면 그리기)  |
+---------------+
       |
       |  requestAnimationFrame
       v
+---------------+
|  콜백 함수   |
|  (애니메이션 처리) |
+---------------+
       |
       |  결과 반영
       v
+---------------+
|  화면 업데이트  |
+---------------+
```

### 코드로 이해하기
```typescript
// requestAnimationFrame 사용 예
function animate() {
  // 애니메이션 처리
  requestAnimationFrame(animate);
}
animate();

// setTimeout 사용 예
function animate() {
  // 애니메이션 처리
  setTimeout(animate, 1000/60); // 60FPS를 가정
}
animate();
```

```typescript
// 잘못된 사용 예: requestAnimationFrame을 반복적으로 호출하지 않는 경우
function animate() {
  // 애니메이션 처리
}
requestAnimationFrame(animate);

// 올바른 사용 예: requestAnimationFrame을 recursive하게 호출
function animate() {
  // 애니메이션 처리
  requestAnimationFrame(animate);
}
requestAnimationFrame(animate);
```

### 비교 분석

| 구분 | requestAnimationFrame | setTimeout |
|------|------------------------|------------|
| 동작 방식 | 브라우저의_refresh_ 주기와 연결 | 지정된 시간 후에 실행 |
| 성능 | 더 나은 성능과 최적화 | 성능이 requestAnimationFrame보다 낮을 수 있음 |
| 애니메이션 평활도 | 더 높은 평활도 | 평활도는 setTimeout의 정확도에 의존 |

### 실전 팁
- Best Practice: 애니메이션 구현에는 requestAnimationFrame을 사용하고, 단순한 지연이 필요한 경우에는 setTimeout을 사용하는 것이 좋다. 
- 흔한 실수와 해결법: requestAnimationFrame을 recursive하게 호출하지 않는 경우 애니메이션이 정지할 수 있다. 이를 해결하려면 애니메이션 처리 후 requestAnimationFrame을 다시 호출해야 한다.
- 성능 관련 주의사항: 애니메이션을 구현할 때는 브라우저의 렌더링 주기에 맞춰 동작하도록 하는 것이 중요하다. requestAnimationFrame은 이러한 최적화를 자동으로 제공한다.

### 한 줄 정리
requestAnimationFrame과 setTimeout은 애니메이션 구현과 지연 동작을 위한 두 가지 주요 기술이나, 성능과 동작 방식에서 차이점이 있어 사용 목적에 따라 적절하게 선택해야 한다.