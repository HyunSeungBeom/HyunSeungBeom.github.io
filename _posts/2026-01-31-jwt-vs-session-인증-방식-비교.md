---
title: "[Deep Dive] JWT vs Session 인증 방식 비교"
date: 2026-01-31 08:08:55 +0900
categories: [개발뉴스]
tags: [CS, 심화]
---

## 표면적 이해
인증 방식 중 JWT와 Session을 비교하는 방법론입니다.

## Deep Dive

### 왜 필요한가?
- 인증을 처리하려면 사용자의 을 확인해야 하며, 이 과정을 효율적이고 보안적으로 처리하는 데 필요합니다.
- 이전 방식의 한계는 사용자 수가 많아질수록 서버 부하가 증가하고, 보안에 취약한 경우가 많았습니다.

### 내부 동작 원리
- JWT는 Header, Payload, Signature로 구성된 토큰을 생성하여 클라이언트와 서버가 인증 정보를 주고받습니다.
- Session은 서버에 세션을 생성하여 클라이언트가 요청할 때마다 세션을 확인합니다.
```
+---------------+
|  클라이언트  |
+---------------+
         |
         |  로그인 요청
         v
+---------------+
|  서버(로그인) |
+---------------+
         |
         |  JWT 생성
         v
+---------------+
|  클라이언트  |
|  (JWT 보관)  |
+---------------+
         |
         |  요청
         v
+---------------+
|  서버(인증)  |
|  (JWT 확인)  |
+---------------+
```

### 코드로 이해하기
```typescript
// JWT 생성
import jwt from 'jsonwebtoken';
const token = jwt.sign({ userId: 1 }, 'secretKey', { expiresIn: '1h' });

// JWT 인증
import jwt from 'jsonwebtoken';
const decoded = jwt.verify(token, 'secretKey');
```

```typescript
// 잘못된 사용 예: 토큰을 localStorage에 저장
localStorage.setItem('token', token);

// 올바른 사용 예: 토큰을 HTTPOnly 쿠키에 저장
const cookie = `token=${token}; HttpOnly`;
```

### 비교 분석

| 구분 | JWT | Session |
|------|---|---|
| 보안 | 중간 | 낮음 |
| 성능 | 높음 | 낮음 |
| 확장성 | 높음 | 낮음 |

### 실전 팁
- Best Practice: 토큰을 HTTPOnly 쿠키에 저장하여 XSS 공격을 방지합니다.
- 흔한 실수: 토큰을 localStorage에 저장하여 XSS 공격에 노출됩니다.
- 성능 관련 주의사항: 토큰의 유효성을 확인할 때, DB 쿼리를 최소화하여 성능을 높입니다.

### 한 줄 정리
JWT와 Session은 각각의 특성을 가지며, 보안과 성능을 고려하여 적절한 인증 방식을 선택해야 합니다.