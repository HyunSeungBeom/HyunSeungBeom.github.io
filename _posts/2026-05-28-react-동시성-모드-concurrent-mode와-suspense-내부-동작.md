---
title: "[Deep Dive] React 동시성 모드 (Concurrent Mode)와 Suspense 내부 동작"
date: 2026-05-28 08:30:29 +0900
categories: [개발뉴스]
tags: [CS, 심화]
---

## 표면적 이해
React의 동시성 모드(Concurrent Mode)와 Suspense는React 어플리케이션의 성능과 사용자 경험이 개선되도록 설계된 기능입니다.

## Deep Dive

### 왜 필요한가?
React는 초기에 싱글 쓰레드 환경에서 동작하도록 설계되었습니다. 하지만 웹 어플리케이션의 복잡성 증가와 사용자 요구 사항의 다양화로 인해, 싱글 쓰레드 환경에서는 성능과 사용자 경험의 한계가 노출되었습니다. 이에 대응하기 위해 등장한 기술이 바로 동시성 모드와 Suspense입니다. 동시성 모드는 여러 작업을 동시에 처리할 수 있도록 해주며, Suspense는 데이터 로딩 중에 사용자에게 피드백을 주는 방법을 제공합니다.

### 내부 동작 원리
동시성 모드와 Suspense의 내부 동작 원리를 이해하기 위해 다음의 ASCII 다이어그램을 참조하세요.
```
          +---------------+
          |  React Core  |
          +---------------+
                  |
                  |
                  v
          +---------------+
          |  Renderer     |
          |  (DOM, Canvas) |
          +---------------+
                  |
                  |
                  v
          +---------------+
          |  Concurrent    |
          |  Mode (Lane)   |
          +---------------+
                  |
                  |
                  v
          +---------------+
          |  Suspense      |
          |  (Boundary)    |
          +---------------+
                  |
                  |
                  v
          +---------------+
          |  Data Loading  |
          |  (API, Cache)  |
          +---------------+
```
위 다이어그램에서 있듯이, 동시성 모드는 React Core와 Renderer 사이에서 동작하며, Suspense는 데이터 로딩 중에 사용자에게 피드백을 주는 역할을 합니다.

### 코드로 이해하기
다음의 typescript 예제 코드를 참조하세요.
```typescript
import React, { useState, Suspense } from 'react';

const DataFetch = () => {
  const [data, setData] = useState(null);

  const fetchData = async () => {
    const response = await fetch('https://api.example.com/data');
    const json = await response.json();
    setData(json);
  };

  return (
    <Suspense fallback={<div>Loading...</div>}>
      {data && <div>{data}</div>}
      <button onClick={fetchData}>Fetch Data</button>
    </Suspense>
  );
};
```
위 예제 코드에서 Suspense를 사용하여 데이터 로딩 중에 사용자에게 "Loading..."이라는 메시지를 표시합니다.

### 비교 분석
다음 표에서 다양한 기술 특성을 비교 분석해보겠습니다.

| 구분 | React 16 | React 17 | Concurrent Mode |
|------|----------|----------|-----------------|
| 성능  | 싱글 쓰레드 | 싱글 쓰레드 | 멀티 쓰레드   |
| 사용자 경험 | 제한적    | 제한적    | 개선됨        |
| Suspense 지원 | keine    | keine    | 지원          |

### 실전 팁
- Concurrent Mode와 Suspense를 사용할 때는 반드시 성능 테스트를 수행하여 최적화를 진행하세요.
- 잘못된 사용 예: Concurrent Mode를 사용하여 너무 많은 작업을 동시에 처리하는 경우, 성능이 저하될 수 있습니다.
- 올바른 사용 예: Concurrent Mode를 사용하여 데이터 로딩과 렌더링을 동시에 처리하여 사용자 경험을 개선하세요.

### 한 줄 정리
React의 동시성 모드와 Suspense는 현대 웹 어플리케이션의 성능과 사용자 경험을 개선하는 데 중요한 역할을 합니다.