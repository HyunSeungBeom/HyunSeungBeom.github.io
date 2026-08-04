---
title: "[Deep Dive] 브라우저 캐싱 전략 (Memory Cache, Disk Cache, Service Worker Cache)"
date: 2026-08-04 09:08:18 +0900
categories: [개발뉴스]
tags: [CS, 심화]
---

## 표면적 이해
브라우저 캐싱 전략은 웹 페이지의 로딩 속도와 성능을 개선하는 데 중요한 역할을 하는 기술입니다.

## Deep Dive

### 왜 필요한가?
- 브라우저 캐싱은 사용자가 동일한 페이지를 여러 번 방문할 때, 매번 서버에서 데이터를 불러오는 것을 피하여 로딩 속도를 향상시킵니다.
- 이전 방식에서는 매번 페이지를 불러올 때 서버에 요청을 하는데, 이는 서버의 부담과 네트워크 대역폭을 증가시켜 성능을 저하시킵니다.

### 내부 동작 원리
- 브라우저 캐싱은 Memory Cache, Disk Cache, Service Worker Cache 등 여러 가지 유형으로 나뉩니다.
- Memory Cache는 RAM에 데이터를하여 빠른 접근이 가능합니다.
- Disk Cache는 하드디스크에 데이터를 저장하여 영구적인 저장이 가능합니다.
- Service Worker Cache는 웹 애플리케이션에서작업을 지원하는 캐싱 기술입니다.

```
+---------------+
|  웹 페이지  |
+---------------+
          |
          |  요청
          v
+---------------+
| 브라우저 내부 |
|  (Memory Cache) |
+---------------+
          |
          |  캐시 확인
          v
+---------------+
|  서버 요청  |
+---------------+
          |
          |  응답
          v
+---------------+
|  브라우저 내부 |
|  (Disk Cache)  |
+---------------+
          |
          |  캐시 저장
          v
+---------------+
|  서비스 워커  |
|  (Service Worker)|
+---------------+
```

### 코드로 이해하기

```typescript
// Memory Cache 사용 예
const cache = caches.open('my-cache');
cache.then((cache) => {
  cache.put('key', 'value');
});

// Disk Cache 사용 예
const diskCache = caches.open('my-disk-cache');
diskCache.then((diskCache) => {
  diskCache.put('key', 'value');
});

// Service Worker Cache 사용 예
navigator.serviceWorker.register('sw.js')
  .then((registration) => {
    registration.addEventListener('install', (event) => {
      event.waitUntil(
        caches.open('my-sw-cache').then((cache) => {
          return cache.addAll([
            '/index.html',
            '/style.css',
            '/script.js',
          ]);
        }),
      );
    });
  });
```

```typescript
// 잘못된 사용 예: 캐시를 초기화하지 않음
// 올바른 사용 예: 캐시를 초기화함
caches.open('my-cache').then((cache) => {
  cache.put('key', 'value');
  cache.delete('old-key');
});
```

### 비교 분석

| 구분 | Memory Cache | Disk Cache | Service Worker Cache |
|------|--------------|------------|---------------------|
| 저장 위치 | RAM | 하드디스크 | 하드디스크 |
| 접근 속도 | 빠름 | 느림 | 느림 |
| 데이터 보존 기간 | 브라우저 종료시 삭제 | 브라우저 종료시 삭제 | 브라우저 종료시 삭제 |

### 실전 팁
- 캐시 만료 기간을 적절히 설정하여 캐시가 너무 오래 보존되지 않도록 합니다.
- 캐시 키를 유일하고 일관되게 관리하여 캐시 충돌을 피합니다.
- 서비스 워커를 사용하여작업을 지원할 수 있습니다.

### 한 줄 정리
브라우저 캐싱은 웹 페이지의 로딩 속도와 성능을 개선하는 데 중요한 역할을 하는 기술입니다.