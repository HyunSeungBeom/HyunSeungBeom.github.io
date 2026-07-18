---
title: "[Deep Dive] AWS S3 + CloudFront 정적 웹 호스팅 최적화"
date: 2026-07-19 08:53:33 +0900
categories: [개발뉴스]
tags: [CS, 심화]
---

## 표면적 이해
AWS S3와 CloudFront를 이용한 정적 웹 호스팅 최적화는 사용자의 요청에 빠르게 응답하고, 비용을 절약하는 방법이다.

## Deep Dive

### 왜 필요한가?
- 이 기술이 해결하는 문제: 사용자 요청에 빠르게 응답하고, 비용을 절약하는 문제를 해결한다.
- 이전 방식의 한계: 기존의 웹 호스팅 방식은 사용자 요청에 따른 부하가 높고, 응답 시간이다는 문제가 있었다.

### 내부 동작 원리
- 핵심 메커니즘 설명: AWS S3를 사용하여 정적 웹 페이지를 저장하고, CloudFront를 사용하여 콘텐츠를 캐싱하고 분산한다.
- ASCII 다이어그램으로 시각화:
```
                      +---------------+
                      |  사용자 요청  |
                      +---------------+
                             |
                             |
                             v
                      +---------------+
                      |  CloudFront  |
                      |  (캐싱 및 분산) |
                      +---------------+
                             |
                             |
                             v
                      +---------------+
                      |  AWS S3      |
                      |  (정적 웹 페이지) |
                      +---------------+
```

### 코드로 이해하기
```typescript
import * as AWS from 'aws-sdk';

// AWS S3 클라이언트 생성
const s3 = new AWS.S3({
  region: 'ap-northeast-2',
});

// CloudFront 클라이언트 생성
const cloudFront = new AWS.CloudFront({
  region: 'ap-northeast-2',
});

// 정적 웹 페이지 업로드
s3.putObject({
  Bucket: 'my-bucket',
  Key: 'index.html',
  Body: 'Hello World!',
}, (err, data) => {
  if (err) {
    console.log(err);
  } else {
    console.log(data);
  }
});

// CloudFront datm 생성
cloudFront.createDistribution({
  DistributionConfig: {
    Origins: {
      Quantity: 1,
      Items: [
        {
          Id: 'my-origin',
          DomainName: 'my-bucket.s3.ap-northeast-2.amazonaws.com',
          S3OriginConfig: {
            OriginAccessIdentity: '',
          },
        },
      ],
    },
    DefaultCacheBehavior: {
      ForwardedValues: {
        QueryString: false,
        Cookies: {
          Forward: 'none',
        },
      },
      TrustedSigners: {
        Enabled: false,
        Quantity: 0,
      },
      ViewerProtocolPolicy: 'allow-all',
      MinTTL: 0,
    },
    DefaultRootObject: 'index.html',
  },
}, (err, data) => {
  if (err) {
    console.log(err);
  } else {
    console.log(data);
  }
});
```

### 비교 분석

| 구분 | S3 만 사용 | CloudFront 사용 | S3 + CloudFront 사용 |
|------|---------|---------------|--------------------|
| 성능 | 낮음    | 중간          | 최고               |
| 비용 | 높은    | 중간          | 낮음               |
| 복잡도 | 낮음    | 중간          | 낮음               |

### 실전 팁
- Best Practice: CloudFront를 사용하여 캐싱 및 분산을 최적화하고, S3를 사용하여 정적 웹 페이지를 저장한다.
- 흔한 실수와 해결법: CloudFront 배포가 잘못되어 사용자 요청이하거나, S3 버킷 정책이 올바르지 않아 접근이 거부되는 경우가 있다.
- 성능 관련 주의사항: 캐싱 및 분산을 최적화하여 사용자 요청에 빠르게 응답하도록 한다.

### 한 줄 정리
AWS S3와 CloudFront를 이용한 정적 웹 호스팅 최적화는 빠른 응답 시간과 낮은 비용을 제공하는 방법이다.