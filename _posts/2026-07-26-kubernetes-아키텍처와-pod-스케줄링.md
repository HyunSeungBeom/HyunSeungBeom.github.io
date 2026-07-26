---
title: "[Deep Dive] Kubernetes 아키텍처와 Pod 스케줄링"
date: 2026-07-26 09:00:43 +0900
categories: [개발뉴스]
tags: [CS, 심화]
---

## 표면적 이해
Kubernetes 아키텍처와 Pod 스케줄링은 컨테이너 기반의 확장성과 안정성을 제공하는 데 중요한 역할을 합니다.

## Deep Dive

### 왜 필요한가?
- Pod 스케줄링은 클러스터의 리소스를 효율적으로 사용하고 안정성과 확장성을 제공하는 데 중요한 역할을 합니다. 이전 방식의 한계는 클러스터의 리소스를 수동으로 관리해야 하거나, 비용이 많이 드는 하드웨어를 사용해야 하거나, 안정성과 확장성이 부족했습니다.

### 내부 동작 원리
- Kubernetes의 핵심 메커니즘은 컨트롤 플레인과 워커 노드의 상호 작용입니다. 컨트롤 플레인은 클러스터의 상태를 관리하고, 워커 노드는 실제 컨테이너를 실행합니다. Pod 스케줄링은 컨트롤 플레인에서 워커 노드로 Pod를 할당하는 과정을 의미합니다.
```
+---------------+
|  컨트롤 플레인  |
+---------------+
           |
           |
           v
+---------------+
|  워커 노드    |
|  (Pod 실행)  |
+---------------+
           |
           |
           v
+---------------+
|  컨테이너 런타임  |
|  (docker, rkt)  |
+---------------+
```

### 코드로 이해하기
```typescript
// kubernetes-api를 사용하여 Pod를 생성하는 예제
import * as k8s from '@kubernetes/client-node';

const k8sApi = new k8s.KubeConfig();
k8sApi.loadFromDefault();

const pods = k8sApi.makeApiClient(k8s.CoreV1Api);
const namespace = 'default';
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
        image: 'nginx:latest',
      },
    ],
  },
};

pods.createNamespacedPod(namespace, pod).then((res) => {
  console.log(`Pod ${res.body.metadata.name} created`);
}).catch((err) => {
  console.error(err);
});
```

```typescript
// 잘못된 사용 예
// Pod를 생성할 때, spec 필드를 누락한 경우
const pod = {
  apiVersion: 'v1',
  kind: 'Pod',
  metadata: {
    name: 'example-pod',
  },
};

// 올바른 사용 예
// Pod를 생성할 때, spec 필드를 포함한 경우
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
        image: 'nginx:latest',
      },
    ],
  },
};
```

### 비교 분석

| 구분 | ReplicaSet | Deployment | StatefulSet |
|------|-----------|------------|-------------|
| 특성1 | 동일한 Pod를 여러 개 생성 | Pod의 업데이트를 관리 | 순서가 중요한 Pod를 관리 |
| 특성2 | 수신된 요청을 동일하게 분배 | rollout과 rollback을 지원 | Pod의 이름과 호스트 이름을 관리 |

### 실전 팁
- Best Practice: Pod를 생성할 때, spec 필드를 포함하고, containers 필드를 지정하여 컨테이너를 정의해야 합니다.
- 흔한 실수와 해결법: Pod를 생성할 때, spec 필드를 누락하는 경우, `InvalidRequest` 오류가 발생합니다. 해결는 spec 필드를 포함하여 Pod를 생성하는 것입니다.
- 성능 관련 주의사항: Pod를 생성할 때, resource request와 limit을 지정하여 성능을 최적화할 수 있습니다.

### 한 줄 정리
Kubernetes의 Pod 스케줄링은 컨테이너 기반의 확장성과 안정성을 제공하는 데 중요한 역할을 하며, 컨트롤 플레인과 워커 노드의 상호 작용을 통해 작동합니다.