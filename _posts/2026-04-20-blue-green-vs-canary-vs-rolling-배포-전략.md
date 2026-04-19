---
title: "[Deep Dive] Blue-Green vs Canary vs Rolling 배포 전략"
date: 2026-04-20 08:14:21 +0900
categories: [개발뉴스]
tags: [CS, 심화]
---

## 표면적 이해
Blue-Green, Canary, Rolling 배포 전략은 소프트웨어 배포를 위한 전략으로, 각기 다른 목적과 특징을 가지고 있으며, 소프트웨어 배포의 안정성과 신뢰성을 높이는 데 사용됩니다.

## Deep Dive

### 왜 필요한가?
- 소프트웨어 개발에서 새로운 버전의 배포 시 기존 시스템에 영향을 주지 않는 방법이 필요합니다. 기존 시스템은 사용자에 의해 지속적으로 사용되고 있는 서비스를 제공하기 때문입니다.
- 이전 방식에서는 전체 시스템을 중단하고 새로운 버전으로 교체하는 방법을 사용했지만, 이는 서비스 중단의 문제를 야기했습니다.

### 내부 동작 원리
- Blue-Green 배포 전략은 두 개의 동일한 환경(블루, 그린)을 유지하며, 하나의 환경에서 새로운 버전을 배포하고, 테스트 및증 후 이를 사용자에게 제공합니다. 사용자 트래픽을 새로운 버전으로 전환 시, 이전 버전은 그린 환경에서 계속 실행되며, 문제가 생긴 경우에는 이전 버전으로 쉽게 롤백을 수행할 수 있습니다.

```
+---------------+
|  Blue Environment  |
+---------------+
           |
           |  사용자 트래픽
           v
+---------------+
|  Router/LB     |
+---------------+
           |
           |  트래픽 분배
           v
+---------------+
|  Green Environment  |
+---------------+
```

### 코드로 이해하기

```typescript
// Router/LB 예제 (typescript)
interface Router {
  route(request: Request): string;
}

class LoadBalancer implements Router {
  private blueEnvironment: string;
  private greenEnvironment: string;

  constructor(blueEnvironment: string, greenEnvironment: string) {
    this.blueEnvironment = blueEnvironment;
    this.greenEnvironment = greenEnvironment;
  }

  route(request: Request): string {
    // 조건에 따라 트래픽 분배
    if (request.header['X-Use-New-Version'] === 'true') {
      return this.greenEnvironment;
    } else {
      return this.blueEnvironment;
    }
  }
}
```

```typescript
// 잘못된 사용 예 (트래픽 분배 로직이 불명확)
class IncorrectLoadBalancer implements Router {
  private environment: string;

  constructor(environment: string) {
    this.environment = environment;
  }

  route(request: Request): string {
    // 항상 같은 환경으로 트래픽을 분배
    return this.environment;
  }
}

// 올바른 사용 예 (조건에 따라 트래픽 분배)
class CorrectLoadBalancer implements Router {
  private blueEnvironment: string;
  private greenEnvironment: string;

  constructor(blueEnvironment: string, greenEnvironment: string) {
    this.blueEnvironment = blueEnvironment;
    this.greenEnvironment = greenEnvironment;
  }

  route(request: Request): string {
    // 조건에 따라 트래픽 분배
    if (request.header['X-Use-New-Version'] === 'true') {
      return this.greenEnvironment;
    } else {
      return this.blueEnvironment;
    }
  }
}
```

### 비교 분석

| 구분 | Blue-Green | Canary | Rolling |
|------|-----------|--------|---------|
| 특성1 | 두 개의 환경을 유지 | 작은 버전의 새로운 버전을 배포 |_incremental 배포 |
| 특성2 | 쉽게 롤백 | 사용자 트래픽의 일부만 새로운 버전으로 분배 | 중단 시간 없이 배포 |

### 실전 팁
- Best Practice: Blue-Green 배포 전략은 새로운 버전의 배포 시 쉽게 롤백을 수행할 수 있어 안정적인 배포를 제공합니다.
- 흔한 실수와 해결법: 트래픽 분배 로직이 불명확할 경우 사용자 트래픽이 올바르게 분배되지 않을 수 있습니다. 이를 해결하기 위해 트래픽 분배 로직을 명확하게 정의해야 합니다.
- 성능 관련 주의사항: Blue-Green 배포 전략을 사용할 경우 두 개의 환경을 유지해야 하므로, 더 많은 시스템 자원이 필요할 수 있습니다.

### 한 줄 정리
Blue-Green, Canary, Rolling 배포 전략은 각기 다른 목적과 특징을 가지고 있으며, 소프트웨어 배포의 안정성과 신뢰성을 높이는 데 사용됩니다.