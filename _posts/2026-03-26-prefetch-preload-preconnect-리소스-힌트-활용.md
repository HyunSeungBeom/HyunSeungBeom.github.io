---
title: "[Deep Dive] Prefetch, Preload, Preconnect 리소스 힌트 활용"
date: 2026-03-26 08:13:13 +0900
categories: [개발뉴스]
tags: [CS, 심화]
---

## 표면적 이해
리소스 힌트는 웹 페이지의 성능을 개선하기 위해 사용되는 기술로, Prefetch, Preload, Preconnect라는 세 가지 방식이 있습니다.

## Deep Dive

### 왜 필요한가?
웹 페이지는 여러 리소스를해야 하며, 이러한 리소스들을 로딩하는 시간이 전체 페이지 로딩 시간의 상당 부분을 차지할 수 있습니다. 이전 방식에서는 이러한 리소스들을 로딩하는 데 많은 시간을 소비했지만, 리소스 힌트를 이용하면 이러한 리소스들을 미리 로딩할 수 있어 웹 페이지의 성능을 개선할 수 있습니다.

### 내부 동작 원리
리소스 힌트는 브라우저가 리소스를 로딩하기 전에 미리 준비할 수 있도록 합니다. Prefetch는 리소스를 로딩하기 전에 DNS를하고, Preload는 리소스를 로딩하기 전에 캐시를 준비하며, Preconnect는 리소스를 로딩하기 전에 Connection을 설정합니다.
```
          +---------------+
          |  웹 페이지   |
          +---------------+
                  |
                  |
                  v
+---------------+       +---------------+
| Prefetch    |       |  Preload    |
|  (DNS)  |       |  (캐시 준비) |
+---------------+       +---------------+
                  |
                  |
                  v
+---------------+       +---------------+
| Preconnect  |       |  리소스 로딩  |
|  (Connection 설정) |       |               |
+---------------+       +---------------+
```

### 코드로 이해하기

```typescript
// Prefetch 예제
<link rel="prefetch" href="https://example.com/resource.css">

// Preload 예제
<link rel="preload" href="https://example.com/resource.css" as="style">

// Preconnect 예제
<link rel="preconnect" href="https://example.com">
```

```typescript
// 잘못된 사용 예: Prefetch를 Preload와 함께 사용
<link rel="prefetch" href="https://example.com/resource.css">
<link rel="preload" href="https://example.com/resource.css" as="style">

// 올바른 사용 예: Prefetch와 Preload를  사용
<link rel="prefetch" href="https://example.com/resource.css">
<link rel="preload" href="https://example.com/another-resource.css" as="style">
```

### 비교 분석

| 구분 | Prefetch | Preload | Preconnect |
|------|---------|---------|------------|
| 기능 | DNS | 캐시 준비 | Connection 설정 |
| 사용 시기 | 리소스 로딩 이전 | 리소스 로딩 이전 | 리소스 로딩 이전 |
| 성능 | 성능 개선 | 성능 개선 | 성능 개선 |

### 실전 팁
- 리소스 힌트를 사용할 때는 리소스의 크기와 로딩 시간을 고려해야 합니다.
- Prefetch와 Preload를 함께 사용할 때는 주의해야 합니다.
- Preconnect는 SSL/TLS 인증서를 사용하는 경우에만 사용해야 합니다.
- 리소스 힌트는 웹 페이지의 성능을 개선할 수 있지만, 잘못된 사용 시 성능을 저하할 수 있으므로 주의해야 합니다.

### 한 줄 정
리소스 힌트는 Prefetch, Preload, Preconnect라는 세 가지 방식으로 웹 페이지의 성능을 개선할 수 있습니다.