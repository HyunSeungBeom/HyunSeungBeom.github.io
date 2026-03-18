---
title: "[Deep Dive] MSW(Mock Service Worker)를 활용한 API Mocking"
date: 2026-03-19 08:10:35 +0900
categories: [개발뉴스]
tags: [CS, 심화]
---

## 표 이해
MSW(Mock Service Worker)는 클라이언트와 서버 사이에서 위치하여 API 요청을 가로채서Mock 응답을 반환하는 기술입니다.

## Deep Dive

### 왜 필요한가?
MSW는 실제 서버가 구축되기 전에 클라이언트 측 개발을 진행할 수 있게 해주며, 서버 개발이 완료된 후에도 테스트와 디버깅을 효율적으로 할 수 있게 도와줍니다. 이전에는 실제 서버를 사용하거나 로컬에서 서버를 구성하여 테스트해야 하는데, 이러한 방법은 시간 소요가 크고, 실제 서버 환경과 다를 수 있습니다.

### 내부 동작 원리
MSW는 Service Worker를 이용하여 클라이언트와 서버 사이에서 위치합니다. 클라이언트에서 API 요청을하면, MSW가 요청을 가로채서 미리 정의된 Mock 응답을 반환합니다.
```
  +---------------+
  |  클라이언트   |
  +---------------+
           |
           |
           v
  +---------------+
  |  MSW (Service  |
  |  Worker)       |
  +---------------+
           |
           |
           v
  +---------------+
  |  실제 서버    |
  +---------------+
```
클라이언트와 실제 서버 사이에서 위치한 MSW는 클라이언트의 요청을 실제 서버로하지 않고, 미리 정의된 응답을 반환합니다.

### 코드로 이해하기
```typescript
// MSW 라이브러리 Import
import { rest } from 'msw';
import { setupServer } from 'msw/node';

// Mock API 정의
const server = setupServer(
  rest.get('/api/user', (req, res, ctx) => {
    return res(ctx.json({ name: 'John Doe' }));
  }),
);

// 테스트 코드에서 사용
test('API 요청 시 Mock 응답 확인', async () => {
  const response = await fetch('/api/user');
  const data = await response.json();
  expect(data.name).toBe('John Doe');
});
```
```typescript
// 잘못된 사용 예: MSW 설정 후 작업하지 않음
const server = setupServer();

// 올바른 사용 예: 미리 정의된 응답을 반환
const server = setupServer(
  rest.get('/api/user', (req, res, ctx) => {
    return res(ctx.json({ name: 'John Doe' }));
  }),
);
```

### 비교 분석
| 구분 | MSW | 실제 서버 사용 | 로컬 서버 구성 |
|------|---|---|---|
| 개발 속도 | 빠름 | 느림 | 중간 |
| 테스트 편리성 | 편리 | 불편 | 중간 |
| 서버 환경 일치 | 낮음 | 높음 | 중간 |

### 실전 팁
- MSW는 개발과 테스트에 주로 사용하므로, 실 서비스에 사용하지 않도록 주의합니다.
- 미리 정의된 응답을 반환하므로, 실제 서버 환경과 다를 수 있습니다.
- 성능 관련 주의사항으로는, MSW를 사용할 때 실제 서버에 요청이 가지 않으므로, 네트워크 지연이나 오류를 시뮬레이션하기 어려울 수 있습니다.

### 한 줄 정리
MSW는 클라이언트와 서버 사이에서 위치하여 API 요청을 가로채서 Mock 응답을 반환하는 기술로서, 개발과 테스트를 효율적으로할 수 있게 도와줍니다.