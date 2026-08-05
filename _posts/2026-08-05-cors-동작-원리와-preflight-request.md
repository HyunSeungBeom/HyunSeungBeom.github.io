---
title: "[Deep Dive] CORS 동작 원리와 Preflight Request"
date: 2026-08-05 09:02:09 +0900
categories: [개발뉴스]
tags: [CS, 심화]
---

## 표면적 이해
CORS는 클라이언트와 서버가 서로 다른 도메인에서 자원을 공유할 수 있도록 하는 기술로, Preflight Request를 통해 요청을 미리 확인하여 보안을 강화한다.

## Deep Dive

### 왜 필요한가?
- 같은 출처에서만 리소스를 공유하는 Same-Origin Policy의 한계를 해결하기 위해 필요한 기술이다.
- 웹 페이지가 서로 다른 도메인의 리소스를 요청할 때 발생하는 보안 문제를 해결한다.

### 내부 동작 원리
- 클라이언트는 서버에 요청을 Preflight Request를 보내어 서버가 해당 요청을 처리할 수 있는지 확인한다.
- 서버는 클라이언트의 Preflight Request에 대한 응답으로 허용할 수 있는 메소드와 헤더를 지정한다.

```
             +---------------+
             |  Client   |
             +---------------+
                   |
                   | Request
                   v
             +---------------+
             | Preflight  |
             |  Request   |
             +---------------+
                   |
                   | Response
                   v
             +---------------+
             |  Server   |
             +---------------+
                   |
                   | Request
                   v
             +---------------+
             |  Actual    |
             |  Request   |
             +---------------+
```

### 코드로 이해하기

```typescript
// CORS를 사용하지 않는 경우
fetch('https://example.com/api/data')
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

```typescript
// CORS를 사용하는 경우
fetch('https://example.com/api/data', {
  method: 'GET',
  headers: {
    'Content-Type': 'application/json'
  }
})
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error(error));
```

### 비교 분석

| 구분 | Same-Origin Policy | CORS |
|------|-------------------|------|
| 출처 | 같은 출처에서만 리소스를 공유 | 서로 다른 도메인에서 리소스를 공유 |
| 보안 | 보안이 강화됨 | 보안을 강화하기 위해 Preflight Request가 필요 |

### 실전 팁
- CORS를 사용할 때는 Preflight Request를 꼭 확인하여 요청을 미리 확인한다.
- CORS를 사용하는 경우, 서버 측에서 CORS를 허용하도록 설정해야 한다.
- CORS를 사용하는 경우, 클라이언트 측에서 요청 헤더를 설정하여 서버가 해당 요청을 처리할 수 있도록 해야 한다.

### 한 줄 정리
CORS는 클라이언트와 서버가 서로 다른 도메인에서 자원을 공유할 수 있도록 하는 기술로, Preflight Request를 통해 요청을 미리 확인하여 보안을 강화한다.