---
title: "[Deep Dive] CORS 동작 원리와 Preflight Request"
date: 2026-02-12 08:11:56 +0900
categories: [개발뉴스]
tags: [CS, 심화]
---

## 표면적 이해
CORS(Cross-Origin Resource Sharing) 동작 원리와 Preflight Request는 다른 도메인의 자원을 요청할 때 발생하는 제한을 해결하는 기술입니다.

## Deep Dive

### 왜 필요한가?
- CORS 기술이 해결하는 문제는 웹 페이지가 다른 도메인의 자원을 요청할 때 발생하는 동일 출처 정책(Same-Origin Policy) 제한입니다.
- 이전 방식의 한계는 모든 자원 요청이 같은 출처에서만 가능해 보안상 취약한 측면이 있었습니다.

### 내부 동작 원리
- CORS의 핵심 메커니즘은 브라우저와 서버가 협력하여 다른 도메인의 자원을 요청할 수 있도록 합니다.
- ASCII 다이어그램으로 시각화하면 다음과 같습니다.
```
                          +---------------+
                          |  브라우저   |
                          +---------------+
                                    |
                                    |  요청
                                    v
                          +---------------+
                          |  Preflight  |
                          |  Request    |
                          +---------------+
                                    |
                                    |  OPTIONS
                                    v
                          +---------------+
                          |  서버      |
                          |  (CORS 지원) |
                          +---------------+
                                    |
                                    |  응답
                                    v
                          +---------------+
                          |  브라우저   |
                          |  (자원 요청) |
                          +---------------+
```

### 코드로 이해하기
```typescript
//Preflight Request 예
const xhr = new XMLHttpRequest();
xhr.open('GET', 'https://example.com/api/data', true);
xhr.withCredentials = true;
xhr.send();

//서버_side CORS 설정 예
const express = require('express');
const app = express();
app.use((req, res, next) => {
    res.header('Access-Control-Allow-Origin', '*');
    res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept');
    if (req.method === 'OPTIONS') {
        res.header('Access-Control-Allow-Methods', 'PUT, POST, PATCH, DELETE, GET');
        return res.status(200).json({});
    }
    next();
});
```
```typescript
//잘못된 사용 예
// cors 허가되지 않은 도메인에서 자원 요청
const xhr = new XMLHttpRequest();
xhr.open('GET', 'https://example.com/api/data', true);
xhr.send();

//올바른 사용 예
// cors 허가된 도메인에서 자원 요청
const xhr = new XMLHttpRequest();
xhr.open('GET', 'https://example.com/api/data', true);
xhr.withCredentials = true;
xhr.send();
```

### 비교 분석
|구분|동일 출처 정책|CORS|
|------|----------|----|
|자원 요청|한 도메인 내에서만 가능|다른 도메인에서도 가능|
|보안|취약|강화|
|요청 방식|단순 요청|Preflight Request + 실제 요청|

### 실전 팁
- Best Practice: CORS 설정은 서버 측에서 처리합니다.
- 흔한 실수와 해결법: CORS 설정을 잊었을 때는 브라우저 콘솔에서 CORS 오류가 발생합니다.
- 성능 관련 주의사항: Preflight Request는 실제 요청보다 먼저 수행되므로 성능에을 줄 수 있습니다.

### 한 줄 정리
CORS는 동일 출처 정책의 제한을 해결하여 다른 도메인의 자원을 요청할 수 있도록 합니다.