---
title: "[Deep Dive] AWS S3 + CloudFront 정적 웹 호스팅 최적화"
date: 2026-02-23 08:08:28 +0900
categories: [개발뉴스]
tags: [CS, 심화]
---

## 표면적 이해
AWS S3와 CloudFront를 이용한 정적 웹 호스팅 최적화는 사용자에게 빠르고 안정적인 웹 서비스를 제공하는 것을 목표로 합니다.

## Deep Dive

### 왜 필요한가?
기존의 정적 웹 호스팅 방식은 사용자와 서버 사이의 거리, 트래픽 양, 네트워크 상태 등으로 인해 속도와 안정성이 떨어질 수 있습니다. 이러한 문제를 해결하기 위해 AWS S3와 CloudFront를 이용한 정적 웹 호스팅 최적화가 필요합니다. 이전 방식의 한계는 사용자에게 제공하는 서비스의 속도와 안정성을 보장하지 못합니다.

### 내부 동작 원리
AWS S3와 CloudFront를 이용한 정적 웹 호스팅 최적화의 핵심 메커니즘은 다음과 같습니다. 사용자가 웹 페이지에 접근할 때, 가장 가까운 CloudFront 엣지 로케이션으로 요청이 전달됩니다. 요청된 리소스가 CloudFront에 캐시되면, 캐시된 리소스가 사용자에게 반환됩니다. 캐시된 리소스가 없다면, CloudFront는 S3에 요청을 전달하고, S3에서 리소스를 받아 사용자에게 반환한 뒤 캐시합니다.

```
                  +---------------+
                  |  사용자 요청  |
                  +---------------+
                            |
                            |
                            v
                  +---------------+
                  | CloudFront    |
                  |  (엣지 로케이션) |
                  +---------------+
                            |
                            |
                            v
                  +---------------+
                  |  캐시 확인    |
                  |  (CloudFront)  |
                  +---------------+
                            |
                            |
                            v
                  +---------------+
                  |  S3에 요청    |
                  |  (리소스 가져오기) |
                  +---------------+
                            |
                            |
                            v
                  +---------------+
                  |  리소스 반환  |
                  |  (CloudFront)  |
                  +---------------+
                            |
                            |
                            v
                  +---------------+
                  |  캐시 저장    |
                  |  (CloudFront)  |
                  +---------------+
```

### 코드로 이해하기
CloudFront와 S3를 사용하여 정적 웹 호스팅을 설정하는 방법은 다음과 같습니다.

```typescript
import * as AWS from 'aws-sdk';

const s3 = new AWS.S3({ region: 'ap-northeast-2' });
const cloudFront = new AWS.CloudFront({ region: 'us-east-1' });

// S3 버킷 생성
const bucketName = 'my-static-website';
s3.createBucket({ Bucket: bucketName }, (err, data) => {
  if (err) {
    console.log(err);
  } else {
    console.log(`버킷 ${bucketName} 생성 완료`);
  }
});

// CloudFront 배포 생성
const distributionConfig = {
  CallerReference: Date.now().toString(),
  DefaultRootObject: 'index.html',
  Origins: {
    Quantity: 1,
    Items: [
      {
        Id: 'my-s3-origin',
        DomainName: `${bucketName}.s3.amazonaws.com`,
        S3OriginConfig: {
          OriginAccessIdentity: '',
        },
      },
    ],
  },
};

cloudFront.createDistribution(
  {
    DistributionConfig: distributionConfig,
  },
  (err, data) => {
    if (err) {
      console.log(err);
    } else {
      console.log(`CloudFront 배포 생성 완료`);
    }
  }
);
```

```typescript
// 잘못된 사용 예
// S3 버킷을 생성하지 않고 CloudFront 배포를 생성하는 경우
const wrongDistributionConfig = {
  CallerReference: Date.now().toString(),
  DefaultRootObject: 'index.html',
  Origins: {
    Quantity: 1,
    Items: [
      {
        Id: 'my-s3-origin',
        DomainName: 'wrong-bucket-name.s3.amazonaws.com',
        S3OriginConfig: {
          OriginAccessIdentity: '',
        },
      },
    ],
  },
};

// 올바른 사용 예
// S3 버킷을 생성한 후 CloudFront 배포를 생성하는 경우
const correctDistributionConfig = {
  CallerReference: Date.now().toString(),
  DefaultRootObject: 'index.html',
  Origins: {
    Quantity: 1,
    Items: [
      {
        Id: 'my-s3-origin',
        DomainName: `${bucketName}.s3.amazonaws.com`,
        S3OriginConfig: {
          OriginAccessIdentity: '',
        },
      },
    ],
  },
};
```

### 비교 분석

| 구분 | AWS S3 | CloudFront | 정적 웹사이트 |
|------|---|---|---|
| 용도 | 클라우드 스토리지 | 콘텐츠 배포 네트워크 | 정적 웹사이트 호스팅 |
| 특성 | 데이터 저장, 버전 관리 | 캐싱, 콘텐츠 배포, SSL/TLS 지원 | 빠르고 안정적인 웹 서비스 제공 |
| 비용 | GB당 비용 | 지역당 비용 | 서비스 이용 빈도에 따라 비용 발생 |

### 실전 팁
- CloudFront와 S3를 사용하여 정적 웹사이트를 호스팅할 때, 캐싱과 콘텐츠 배포를 적절히 설정하여 빠르고 안정적인 웹 서비스를 제공할 수 있습니다.
- 사용자 요청에 대한 응답 시간을 줄이기 위해 CloudFront의 엣지 로케이션을 적절히 설정하여야 합니다.
- CloudFront와 S3를 사용할 때 발생하는 비용을 최적화하기 위해, 캐싱과 콘텐츠 배포를 효율적으로 설정하여야 합니다.

### 한 줄 정리
AWS S3와 CloudFront를 이용한 정적 웹 호스팅 최적화는 사용자에게 빠르고 안정적인 웹 서비스를 제공하는 것을 목표로 합니다.