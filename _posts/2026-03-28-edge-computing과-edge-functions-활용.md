---
title: "[Deep Dive] Edge Computing과 Edge Functions 활용"
date: 2026-03-28 08:12:30 +0900
categories: [개발뉴스]
tags: [CS, 심화]
---

## 표면적 이해
Edge Computing과 Edge Functions는 데이터를 클라우드나 중앙 서버가 아닌 네트워크의 가장자리에서 처리하여 지연 시간을 줄이고 실시간 처리를 가능하게하는 기술입니다.

## Deep Dive

### 왜 필요한가?
- Edge Computing과 Edge Functions는 데이터를 중앙 서버에서 처리하는 전통적인 방식의 제약을 해결합니다. 전통적인 방식은 데이터가 네트워크를 통해 중앙 서버로 전송되어 처리되는데, 이는 지연 시간을 증가시키고 실시간 처리를 어렵게 만듭니다.
- Edge Computing과 Edge Functions는 데이터를 네트워크의 가장자리에서 처리하여 지연 시간을 줄이고 실시간 처리를 가능하게합니다. 이를 통해 IoT, 실시간 분석, 게임 등과 같은 응용 분야에서 큰 성능 향상을 기대할 수 있습니다.

### 내부 동작 원리
- Edge Computing과 Edge Functions의 핵심은 데이터를 네트워크의 가장자리에서 처리하는 것입니다. 이를 위해 Edge 노드라고 불리는 특별한 장치 또는 소프트웨어가 네트워크의 가장자리에 위치합니다.
- Edge 노드는 데이터를 수집하고 처리하여 결과를 바로 클라이언트에 전송하거나, 필요할 경우 중앙 서버에 전송합니다.
- Edge Functions는 Edge 노드에서 실행되는 함수형 프로그래밍의 한 형태입니다.Edge Functions는 데이터를 처리하고 결과를 반환하는 작은 코드 블록으로, Edge 노드에서 실행되어 지연 시간을 최소화합니다.

 ```
  +---------------+
  |  클라이언트   |
  +---------------+
           |
           |
           v
  +---------------+
  |  Edge 노드    |
  |  (Edge Functions)|
  +---------------+
           |
           |
           v
  +---------------+
  |  중앙 서버   |
  +---------------+
```

### 코드로 이해하기
```typescript
// Edge Functions 예제 ( TypeScript )
function edgeFunction(data: string): string {
  // 데이터 처리 로직
  const processedData = data.toUpperCase();
  return processedData;
}

// Edge 노드에서 edgeFunction을 실행
const inputData = "hello";
const result = edgeFunction(inputData);
console.log(result); // OUTPUT: HELLO
```

```typescript
// 잘못된 사용 예
function wrongEdgeFunction(data: string): string {
  // 데이터 처리 로직 (비동기식으로 중앙 서버에 요청)
  fetch("https://central-server.com/process", {
    method: "POST",
    body: data,
  })
    .then((response) => response.text())
    .then((processedData) => {
      return processedData;
    });
}

// 올바른 사용 예
function correctEdgeFunction(data: string): string {
  // 데이터 처리 로직 (동기식으로 Edge 노드에서 처리)
  const processedData = data.toUpperCase();
  return processedData;
}
```

### 비교 분석

| 구분 | Edge Computing | 클라우드 컴퓨팅 | 중앙 서버 |
|------|----------------|---------------|-----------|
| 처리 위치 | 네트워크의 가장자리 | 클라우드 | 중앙 서버 |
| 지연 시간 | thp | 높은 | 높은 |
| 실시간 처리 | 가능 | 어렵움 | 어렵움 |
| 데이터 처리 | Edge 노드 | 클라우드 | 중앙 서버 |

### 실전 팁
- Edge Functions는 작은 코드 블록으로, Edge 노드에서 실행되어 지연 시간을 최소화합니다.
- Edge Computing과 Edge Functions는 데이터를 네트워크의 가장자리에서 처리하여 지연 시간을 줄이고 실시간 처리를 가능하게합니다.
- 잘못된 사용 예는 데이터를 중앙 서버에 요청하는 비동기식 코드로, 올바른 사용 예는 데이터를 Edge 노드에서 처리하는 동기식 코드입니다.

### 한 줄 정리
Edge Computing과 Edge Functions는 데이터를 네트워크의 가장자리에서 처리하여 지연 시간을 줄이고 실시간 처리를 가능하게하는 기술입니다.