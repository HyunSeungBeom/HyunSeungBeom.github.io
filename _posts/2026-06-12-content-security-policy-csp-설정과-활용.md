---
title: "[Deep Dive] Content Security Policy (CSP) 설정과 활용"
date: 2026-06-12 08:34:26 +0900
categories: [개발뉴스]
tags: [CS, 심화]
---

## 표면적 이해
콘텐트 보안 정책(CSP) 설정과 활용은 웹 애플리케이션의 안전성을 강화하기 위한 wicht한 구성 요소이다.

## Deep Dive

### 왜 필요한가?
- CSP는 크로스 사이트 스크립팅(XSS) 공격과 같은 심각한 보안 허점을 막을 수 있게 해준다. 이전 방식은 보안 정책을 정의하고 강제하기 위한 명확한 프레임워크가 부족했는데, CSP는 이러한 결점을 보완한다.

### 내부 동작 원리
- CSP는 웹 브라우저에 서버가 제공하는 콘텐트에대한 규칙을 제공한다. 이 규칙에는 콘텐트를 로드할 수 있는 원천을 명시함으로써 보안을 강화한다. 예를 들어, 특정 도메인에서만 자바스크립트 파일을 로드하는 것을 허용하거나 특정한 스타일시트를 허용하는 방법 등이다.
```
                  +---------------+
                  |  웹 브라우저  |
                  +---------------+
                             |
                             |  요청
                             v
                  +---------------+
                  |  웹 서버    |
                  |  (CSP 헤더)  |
                  +---------------+
                             |
                             |  응답
                             v
                  +---------------+
                  |  웹 브라우저  |
                  |  (CSP 적용)    |
                  +---------------+
```

### 코드로 이해하기
```typescript
// HTTP 응답 헤더에 CSP 정책을 설정하는 방법
const http = require('http');

http.createServer((req, res) => {
  res.writeHead(200, {
    'Content-Security-Policy': "default-src 'self'; script-src 'self' https://cdn.example.com",
  });
  res.end('Hello World!');
}).listen(3000, () => {
  console.log('서버가 시작되었습니다.');
});
```

```typescript
// 잘못된 사용 예: 모든 출처에서 스크립트를 로드하여 XSS 공격에 취약
const http = require('http');

http.createServer((req, res) => {
  res.writeHead(200, {
    'Content-Security-Policy': "script-src *",
  });
  res.end('Hello World!');
}).listen(3000, () => {
  console.log('서버가 시작되었습니다.');
});

// 올바른 사용 예: 특정 도메인에서만 스크립트를 로드
const http = require('http');

http.createServer((req, res) => {
  res.writeHead(200, {
    'Content-Security-Policy': "script-src 'self' https://cdn.example.com",
  });
  res.end('Hello World!');
}).listen(3000, () => {
  console.log('서버가 시작되었습니다.');
});
```

### 비교 분석

| 구분 | CSP 사용 | CSP 미사용 |
|------|---------|-------------|
| 보안성 | 높은 보안성 | 낮은 보안성 |
| 구현 난이도 | 비교적 낮은 난이도 | - |
| XSS 공격 방지 |하게 방지 | 취약 |

### 실전 팁
- CSP를 설정할 때는 가능한 적은 출처만 허용하여 보안을 강화한다.
- CSP는 여러개의 지시자를 지원하므로, 스크립트 출처와 스타일시트 출처 등에 대한 규칙을 개별적으로 정의할 수 있다.
- CSP 설정 시, 'self' 지시자를 사용하여 동일 출처의 콘텐트를 허용할 수 있다.
- CSP를 설정한 후, 브라우저 로그를 살펴보아 CSP 규칙 위반을 식별하고, 필요한 추가 설정을 수행한다.

### 한 줄 정리
콘텐트 보안 정책(CSP)을 설정하고 활용하면 웹 애플리케이션의 보안성을 크게 강화할 수 있다.