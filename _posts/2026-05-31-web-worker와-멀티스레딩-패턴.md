---
title: "[Deep Dive] Web Worker와 멀티스레딩 패턴"
date: 2026-05-31 08:24:50 +0900
categories: [개발뉴스]
tags: [CS, 심화]
---

## 표면적 이해
Web Worker와 멀티스레딩 패턴은 웹 어플리케이션에서 성능 향상을 위한 중요한 기술입니다.

## Deep Dive

### 왜 필요한가?
- 웹 브라우저에서 실행되는스크립트는 싱글 스레드로 동작합니다. 이로 인해 장시간 실행되는 작업은 브라우저의 메인 스레드를 점유하여 사용자 인터페이스의 반응을 늦추게 됩니다.
- 이전 방식은 setTimeout과 같은 함수를 사용하여 작업을 분할하여 처리하거나, 웹 워커를 사용하여 별도의 스레드에서 작업을 처리했습니다. 하지만 이러한 방법은 제한적이었으며, 복잡한 작업을 처리하기 어렵습니다.

### 내부 동작 원리
- Web Worker는 브라우저가 제공하는 별도의 스레드에서 실행되는 스크립트입니다. 이로 인해 메인 스레드와 별개로 작업을 처리할 수 있습니다.
- Web Worker는 메인 스레드와 통신하기 위해 postMessage 함수를 사용합니다. 이 함수를 통해 데이터를 송수신하여 작업을 수행할 수 있습니다.
 
```
         +---------------+
         |  메인 스레드  |
         +---------------+
                  |
                  |  postMessage
                  v
         +---------------+
         |  Web Worker  |
         +---------------+
                  |
                  |  postMessage
                  v
         +---------------+
         |  메인 스레드  |
         +---------------+
```

### 코드로 이해하기

```typescript
// Web Worker 생성
const worker = new Worker('worker.js');

// 메인 스레드에서 Web Worker로 데이터 전송
worker.postMessage({ type: 'start', data: 'Hello, World!' });

// Web Worker에서 수신된 데이터 처리
worker.onmessage = (event) => {
  if (event.data.type === 'result') {
    console.log(`Received result: ${event.data.result}`);
  }
};
```

```typescript
// worker.js
self.onmessage = (event) => {
  if (event.data.type === 'start') {
    const result = performLongRunningTask(event.data.data);
    self.postMessage({ type: 'result', result });
  }
};

function performLongRunningTask(data: string): string {
  // 장시간 실행되는 작업을 수행합니다.
  return `Processed: ${data}`;
}
```

### 비교 분석

| 구분 | Web Worker | 타이머 함수 | Ajax 요청 |
|------|---------|--------|-------|
| 스레드 | 별도의 스레드 | 메인 스레드 | 메인 스레드 |
| 작업 시간 | 제한 없음 | 제한 있음 | 제한 없음 |
| 데이터 전송 | postMessage | 콜백 함수 | 콜백 함수 |

### 실전 팁
- Web Worker를 사용할 때는 메인 스레드와 별도의 스레드이므로 메인 스레드에서 사용한 변수나 함수를 참조할 수 없습니다.
- Web Worker에서 사용하는 스크립트는 별도의 파일로 분리하여 관리해야 합니다.
- Web Worker를 생성할 때는 작업을 처리할 수 있는 시간을 고려하여 생성해야 합니다.

### 한 줄 정리
Web Worker와 멀티스레딩 패턴을 활용하여 웹 어플리케이션의 성능을 향상할 수 있습니다.