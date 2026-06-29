---
title: "[Deep Dive] 프론트엔드 성능 측정과 Lighthouse 점수 최적화"
date: 2026-06-30 08:24:37 +0900
categories: [개발뉴스]
tags: [CS, 심화]
---

## 표면적 이해
프론트엔드 성능 측정과 Lighthouse 점수 최적화는 사용자의 경험을 향상시키는 데 중요한 역할을 합니다.

## Deep Dive

### 왜 필요한가?
- 웹 사이트의 속도와 효율성은 사용자의 Satisfaction에 직접적인 영향을 미칩니다. 이전 방식에서는 성능에 대한 고려가 부족하여 사용성이 떨어지는 웹 페이지들이 만들어졌습니다. 
- 따라서 프론트엔드 성능 측정 및 최적화는 더 나은 사용자 경험을 제공하는 데 핵심입니다.

### 내부 동작 원리
- Lighthouse는 웹 페이지의 성능을 측정하는 데 사용되는 인기 있는 도구입니다. Lighthouse는 다양한 카테고리에서 웹 페이지의 점수를 평가합니다. 대표적인 항목으로는 Performance, Accessibility, Best Practices, SEO, PWA가 있습니다.
```
                               +---------------+
                               |  페이지 요청  |
                               +---------------+
                                       |
                                       |
                                       v
                               +---------------+
                               | 웹 페이지 렌더링 |
                               |  (HTML, CSS, JS) |
                               +---------------+
                                       |
                                       |
                                       v
                               +---------------+
                               |  Lighthouse   |
                               |  성능 평가 시작 |
                               +---------------+
                                       |
                                       |
                                       v
                               +---------------+
                               | 성능 점수 산출  |
                               |  (0 ~ 100점)     |
                               +---------------+
```

### 코드로 이해하기

```typescript
// Lighthouse 점수를 최적화하는 방법은 여러 가지가 있습니다. 
// 첫째, 불필요한 자원을 제거하여 페이지 로딩 시간을 단축해야 합니다.
import { optimize } from 'webpack';

// 두번째, 이미지 파일을하여 파일 크기를 줄입니다.
const imgOptimizePlugin = require('image-webpack-loader');

// 세번째, 코드 스플리팅을 적용하여 초기 렌더링에 필요한 자원을 줄입니다.
import React from 'react';
import { BrowserRouter, Route, Routes } from 'react-router-dom';

const App = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
      </Routes>
    </BrowserRouter>
  );
};

// 잘못된 사용 예: 불필요한 자원 로딩
// const allData = require('./all-data.json');
// 올바른 사용 예: 필요한 자원만 로딩
const neededData = require('./needed-data.json');

// 성능 최적화 예
const isDevelopment = process.env.NODE_ENV === 'development';

if (isDevelopment) {
  // 개발 환경에서는 성능 최적화 기능을 비활성화 할 수 있습니다.
} else {
  // 프로덕션 환경에서는 성능 최적화 기능을 활성화합니다.
}
```

### 비교 분석

| 구분 | 일반적인 웹 사이트 | 최적화된 웹 사이트 | Lighthouse 점수 |
|------|-----------|-----------|---------|
| 로딩 시간 | 5초 이상 | 2초 이하 | 90점 이상 |
| 이미지 파일 크기 | 1MB 이상 | 100KB 이하 | 80점 이상 |
| 코드 스플리팅 | 미적용 | 적용 | 95점 이상 |

### 실전 팁
- 성능 최적화를 위해 먼저 웹 페이지의 로딩 시간을 단축하세요.
- 이미지 파일을하고 코드 스플리팅을 적용하세요.
- Lighthouse 점수를 정기적으로 확인하여 웹 페이지의 성능을 모니터링하세요.
- 불필요한 자원을 제거하고, 사용자 경험을 향상시키는 기능을 추가하세요.

### 한 줄 정리
Lighthouse를 사용하여 웹 페이지의 성능을 평가하고, 최적화를 통해 사용자 Satisfaction을 향상시킵니다.