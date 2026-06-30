---
title: "[Deep Dive] MSW(Mock Service Worker)를 활용한 API Mocking"
date: 2026-07-01 08:30:38 +0900
categories: [개발뉴스]
tags: [CS, 심화]
---

## 표면적 이해
MSW(Mock Service Worker)를 활용한 API Mocking은 개발 중에 실제 API 서버 없이도 클라이언트 쪽 개발을 진행할 수 있도록 해주는 기술입니다.

## Deep Dive

### 왜 필요한가?
API Mocking이 필요한 이유는 실제 개발 과정에서 발생하는 문제점을 해결하기 위함입니다. 실제 API 서버 없이 개발을 진행할 때, 개발자들은 다음과 같은 문제에 직면할 수 있습니다: 
- 실제 API 서버의 대기가 길어 개발 속도가 늦어질 수 있습니다.
- 실제 API 서버가 없는 경우 개발이 중단될 수 있습니다.
- 일부 기능은 실제 API 서버와 연동되어 있어 테스트가 어려울 수 있습니다.

이전 방식의 한계는 개발자들이 실제 API 서버를 구축하거나, 기존 API를 사용해야만 개발을 진행할 수 있었던 점입니다. 하지만 MSW를 활용하면 개발 중에 실제 API 없이도 Mock API를 쉽게 구축할 수 있어 개발 속도를 향상하고 비용을 절감할 수 있습니다.

### 내부 동작 원리
MSW는 Service Worker를 기반으로 동작합니다. Service Worker는 브라우저의 네트워크 요청을 가로채서 처리할 수 있는 기술입니다. MSW는 이 기술을 활용하여 HTTP 요청을 가로채고, 미리 정의된 응답 값을 반환합니다.

```
+---------------+
|  Web Application  |
+---------------+
            |
            |  (HTTP Request)
            v
+---------------+
|  Service Worker  |
|  (MSW)         |
+---------------+
            |
            |  (Mock Response)
            v
+---------------+
|  Browser         |
+---------------+
```

### 코드로 이해하기
다음은 MSW를 사용하여 간단한 API Mocking을 구현한 예시입니다.

```typescript
import { setupServer } from 'msw/node';
import { rest } from 'msw';

const server = setupServer(
  rest.get('/api/user', (req, res, ctx) => {
    return res(ctx.json({ name: 'John Doe' }));
  }),
);

// 실제 동작을 보여주는 코드 예제
server.listen();
```

```typescript
// 잘못된 사용 예
// MSW를 사용하지 않고 실제 API를 호출하는 경우
fetch('/api/user')
  .then((res) => res.json())
  .then((data) => console.log(data));

// 올바른 사용 예
// MSW를 사용하여 Mock API를 호출하는 경우
setupServer(
  rest.get('/api/user', (req, res, ctx) => {
    return res(ctx.json({ name: 'John Doe' }));
  }),
);
fetch('/api/user')
  .then((res) => res.json())
  .then((data) => console.log(data));
```

### 비교 분석

| 구분 | 실제 API | Mock API |
|------|---------|----------|
| 개발 속도 | 느림      | 빠름      |
| 비용     | 높음      | 낮음      |
| 복잡도   | 높음      | 낮음      |

### 실전 팁
- Best Practice: MSW를 사용할 때는 항상 Server를 정지하는 것을 잊지 마세요.
- 흔한 실수와 해결법: MSW의 요청을 처리하는 함수가 반환하지 않을 경우, 요청이 지연되는 현상이 발생할 수 있습니다. 이러한 경우, 함수가 올바르게 반환되는지 확인하세요.
- 성능 관련 주의사항: MSW는 Service Worker를 기반으로 동작합니다. 따라서 Service Worker의 제약사항을 숙지하여야 합니다.

### 한 줄 정리
MSW(Mock Service Worker)를 활용한 API Mocking은 개발 중에 실제 API 서버 없이도 클라이언트 쪽 개발을 진행할 수 있도록 해주는 기술입니다.