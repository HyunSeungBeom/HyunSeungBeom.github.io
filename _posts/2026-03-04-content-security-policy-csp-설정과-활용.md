---
title: "[Deep Dive] Content Security Policy (CSP) 설정과 활용"
date: 2026-03-04 08:08:37 +0900
categories: [개발뉴스]
tags: [CS, 심화]
---

## 표면적 이해
Content Security Policy (CSP)는 웹페이지의 보안을 강화하기 위한 정책으로, 외부 스크립트와 스타일시트를 제어하는 기능을 제공합니다.

## Deep Dive

### 왜 필요한가?
- Content Security Policy (CSP)는 웹페이지가 외부Attack으로부터 보호되도록 설계되었습니다. 이전 방식에서는 HTML 태그 안에 자바스크립트 코드나 CSS 스타일시트가 포함되어 있으면, 이들을 공격자들이 악용할 수 있는 취약점이 있었습니다. CSP는 이러한 취약점을 제거하고, 웹페이지의 보안을 강화합니다.

### 내부 동작 원리
- CSP는 웹페이지에서 외부 스크립트와 스타일시트를 로드할 때 사용하는 정책입니다. CSP가 설정되면, 브라우저는 해당 정책에 따라 외부 스크립트와 스타일시트를 로드하거나 차단합니다.
```
          +---------------+
          |  웹페이지    |
          +---------------+
                  |
                  |  CSP 설정
                  v
          +---------------+
          |  브라우저    |
          |  (외부 스크립트와 |
          |   스타일시트 로드) |
          +---------------+
                  |
                  |  정책 확인
                  v
          +---------------+
          |  외부 스크립트와  |
          |  스타일시트 로드  |
          |  (정책에 따라)    |
          +---------------+
```

### 코드로 이해하기

```typescript
// HTML 헤더에 CSP 설정
const csp = "default-src 'self'; script-src 'self' https://cdn.example.com; object-src 'none'";
const metaTag = document.createElement('meta');
metaTag.httpEquiv = 'Content-Security-Policy';
metaTag.content = csp;
document.head.appendChild(metaTag);
```

```typescript
// 잘못된 사용 예
const wrongCsp = "default-src *";
const wrongMetaTag = document.createElement('meta');
wrongMetaTag.httpEquiv = 'Content-Security-Policy';
wrongMetaTag.content = wrongCsp;
document.head.appendChild(wrongMetaTag);

// 올바른 사용 예
const correctCsp = "default-src 'self'; script-src 'self' https://cdn.example.com; object-src 'none'";
const correctMetaTag = document.createElement('meta');
correctMetaTag.httpEquiv = 'Content-Security-Policy';
correctMetaTag.content = correctCsp;
document.head.appendChild(correctMetaTag);
```

### 비교 분석

| 구분 | CSP | CORS | SSL/TLS |
|------|---|---|---|
| 특성1 | 웹페이지 보안 강화 | 도메인 간 리소스 공유 | 데이터 암호화 |
| 특성2 | 외부 스크립트와 스타일시트 제어 | HTTP 헤더 설정 | 암호화 프로토콜 |

### 실전 팁
- Best Practice: CSP 설정을 웹페이지의 헤더에 추가합니다. 외부 스크립트와 스타일시트를 로드하는 경우, 정책에 따라 로드하도록 설정합니다.
- 흔한 실수와 해결법: 외부 스크립트와 스타일시트를 로드하는 경우, 정책에 따라 로드하지 않으면 오류가 발생할 수 있습니다. 이 경우, 정책을 설정하여 외부 스크립트와 스타일시트를 로드하도록 합니다.
- 성능 관련 주의사항: CSP 설정을 웹페이지의 헤더에 추가하면, 브라우저가 외부 스크립트와 스타일시트를 로드하는 데 시간이 걸릴 수 있습니다. 따라서, 성능을 고려하여 정책을 설정해야 합니다.

### 한 줄 정리
Content Security Policy (CSP)는 웹페이지의 보안을 강화하기 위해 외부 스크립트와 스타일시트를 제어하는 기능을 제공합니다.