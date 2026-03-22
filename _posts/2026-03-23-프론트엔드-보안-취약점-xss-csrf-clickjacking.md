---
title: "[Deep Dive] 프론트엔드 보안 취약점 (XSS, CSRF, Clickjacking)"
date: 2026-03-23 08:09:11 +0900
categories: [개발뉴스]
tags: [CS, 심화]
---

## 표면적 이해
프론트엔드 보안 취약점은 XSS, CSRF, Clickjacking 등의 공격에 노출될 수 있는 취약점을 말합니다.

## Deep Dive

### 왜 필요한가?
- 프론트엔드 보안 취약점은 사용자의 개인정보를 탈취하거나, 악의적인 코드를 실행하는 등의 문제를 해결해야 합니다. 이전에는 이러한 보안 취약점에 대한 인식이 부족하여 큰 문제가 없다고 생각해 왔지만, 최근에 들어와서는 이러한 취약점이 더욱 심각해졌습니다.

### 내부 동작 원리
- XSS(크로스 사이트 스크립팅)은 attacker가 사용자의 브라우저에 악의적인 코드를 실행시키는 것입니다. 이를 방지하기 위해 사용하는 것이 Content Security Policy(CSP)입니다.
```
                          +---------------+
                          |  사용자 브라우저  |
                          +---------------+
                                    |
                                    |  요청
                                    v
                          +---------------+
                          |  서버          |
                          |  (CSP 설정)    |
                          +---------------+
                                    |
                                    | 응답
                                    v
                          +---------------+
                          |  사용자 브라우저  |
                          |  (CSP 적용)     |
                          +---------------+
```

### 코드로 이해하기

```typescript
// CSP 설정 예
const csp = 'default-src \'self\'; script-src \'self\' https://cdn.example.com;';
```

```typescript
// 잘못된 사용 예
// CSP 설정을 생략한 경우
const csp = '';

// 올바른 사용 예
// CSP 설정을 적절히 설정한 경우
const csp = 'default-src \'self\'; script-src \'self\' https://cdn.example.com;';
```

### 비교 분석

| 구분 | XSS | CSRF | Clickjacking |
|------|-----|------|--------------|
| 원인 | 악의적인 코드 실행 | 사용자의 요청 조작 | 사용자의 클릭 조작 |
| 결과 | 개인정보 탈취 | 악의적인 요청 실행 | 악의적인 코드 실행 |
| 예방 | CSP 설정, 입력값 검증 | token 사용, SameSite 속성 | iframe 사용 금지, X-Frame-Options 설정 |

### 실전 팁
- CSP 설정은 default-src를 사용해 기본 소스를 설정하고, script-src를 사용해 스크립트 소스를 설정합니다.
- 입력값을 검증하여 악의적인 코드를 방지합니다.
- SameSite 속성을 사용하여 CSRF 공격을 방지합니다.
- iframe 사용을 금지하고, X-Frame-Options를 설정하여 Clickjacking 공격을 방지합니다.

### 한 줄 정리
프론트엔드 보안 취약점은 XSS, CSRF, Clickjacking 등의 공격에 노출될 수 있는 취약점을 말하며, 이러한 취약점을 해결하기 위해 CSP 설정, 입력값 검증, SameSite 속성 사용, iframe 사용 금지 등의 방법을 사용합니다.