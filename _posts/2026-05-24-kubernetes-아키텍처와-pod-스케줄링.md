---
title: "[Deep Dive] Kubernetes 아키텍처와 Pod 스케줄링"
date: 2026-05-24 08:21:47 +0900
categories: [개발뉴스]
tags: [CS, 심화]
---

## 표면적 이해
Kubernetes 아키텍처와 Pod 스케줄링은 컨테이너 오케스트레이션의 핵심을 이루는 기술로, 다수의 컨테이너를 효율적으로 관리하는 방법을 제공합니다.

## Deep Dive

### 왜 필요한가?
- 이 기술이 해결하는 문제: 컨테이너화된 애플리케이션을 대규모로 관리하여, 가용성과 확장성을 높이는 문제를 해결합니다.
- 이전 방식의 한계: 이전에는 수동으로 컨테이너를 관리하거나, 단순한 스크립트를 이용하여 관리를 하였지만, 이는 효율성이 낮고, 오류가 발생하기 쉽습니다.

### 내부 동작 원리
- 핵심 메커니즘 설명: Kubernetes는 컨테이너를 Pod라는 단위로 묶고, 이 Pod를 여러 노드에 분산하여 관리합니다. 스케줄러는 클러스터의 리소스를 감시하며, 새로생성된 혹은 실행되어야 하는 Pod를 적절한 노드에 할당합니다.
```
            +---------------+
            |  Controller  |
            +---------------+
                     |
                     |  API 요청
                     v
            +---------------+
            |  Scheduler    |
            +---------------+
                     |
                     |  노드 리소스 감시
                     v
            +---------------+
            |  Node          |
            +---------------+
                     |
                     |  Pod 실행
                     v
            +---------------+
            |  Pod           |
            +---------------+
                     |
                     |  컨테이너 실행
                     v
            +---------------+
            |  Container     |
            +---------------+
```

### 코드로 이해하기

```typescript
// Kubernetes 클라이언트 라이브러리를 이용하여, Pod를 생성하는 예
import * as k8s from '@kubernetes/client-node';

const k8sApi = new k8s.Kubernetes({
  config: {
    url: 'https://your-k8s-cluster.com',
    token: 'your-token',
  },
});

const pod = {
  apiVersion: 'v1',
  kind: 'Pod',
  metadata: {
    name: 'example-pod',
  },
  spec: {
    containers: [
      {
        name: 'example-container',
        image: 'example-image',
      },
    ],
  },
};

k8sApi.createNamespacedPod('default', pod).then((res) => {
  console.log(res.body);
}).catch((err) => {
  console.error(err);
});
```

```typescript
// 잘못된 사용 예: Pod를 생성할 때, 적절한 리소스 요청을 하지 않은 경우
const pod = {
  apiVersion: 'v1',
  kind: 'Pod',
  metadata: {
    name: 'example-pod',
  },
  spec: {
    containers: [
      {
        name: 'example-container',
        image: 'example-image',
      },
    ],
  },
};

// 올바른 사용 예: Pod를 생성할 때, 적절한 리소스 요청을 한 경우
const podWithResources = {
  apiVersion: 'v1',
  kind: 'Pod',
  metadata: {
    name: 'example-pod',
  },
  spec: {
    containers: [
      {
        name: 'example-container',
        image: 'example-image',
        resources: {
          requests: {
            cpu: '100m',
            memory: '128Mi',
          },
          limits: {
            cpu: '200m',
            memory: '256Mi',
          },
        },
      },
    ],
  },
};
```

### 비교 분석

| 구분 | Docker Swarm | Kubernetes | Apache Mesos |
|------|-------------|-----------|--------------|
| 특성1 | 간단한 컨테이너 오케스트레이션 | 복잡한 워크로드 관리 | 다중 프레임워크 지원 |
| 특성2 | 노드 관리가 비교적 쉽지만 확장성이 낮음 | 노드 관리가 비교적 복잡하지만 확장성이 높음 | 다중 프레임워크 지원으로 유연함 |

### 실전 팁
- Best Practice: 적절한 리소스 요청과 제한을 설정하여, 클러스터의 안정성을 높입니다.
- 흔한 실수와 해결법: Pod가 종료되었지만, 다시 시작되지 않는 경우, 로그를 확인하여, 에러를 찾고, Pod의 정의를 확인하여, 문제를 해결합니다.
- 성능 관련 주의사항: 클러스터의 노드를하게 로드하면, 성능이 저하되므로, 클러스터의 리소스를 모니터링하고, 노드를 추가로 배포하여, 성능을 높입니다.

### 한 줄 정리
Kubernetes 아키텍처와 Pod 스케줄링은 컨테이너 오케스트레이션의 핵심으로, 효율적인 클러스터 관리와 확장성을 제공합니다.