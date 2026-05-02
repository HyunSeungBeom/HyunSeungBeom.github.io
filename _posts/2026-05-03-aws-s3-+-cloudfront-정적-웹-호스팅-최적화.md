---
title: "[Deep Dive] AWS S3 + CloudFront 정적 웹 호스팅 최적화"
date: 2026-05-03 08:18:30 +0900
categories: [개발뉴스]
tags: [CS, 심화]
---

## 표면적 이해
AWS S3와 CloudFront를 이용해 정적 웹 호스팅의 성능과 보안을 최적화하는 방법을합니다.

## Deep Dive

### 왜 필요한가?
- 정적 웹 호스팅은 사용자에게 빠르고 안정적인 콘텐츠를 제공해야 하며, 이를 위해 최적화된 인프라가 필요합니다. 이전 방식의 한계는 서버의 부하와 지연 시간, 보안 취약성 등의 문제가 있었습니다.

### 내부 동작 원리
- AWS S3는 객체 서비스로, 정적 웹 콘텐츠를 효율적으로 저장하고 관리할 수 있습니다. CloudFront는 콘텐츠 전송 네트워크(CDN) 서비스로, 사용자와 가장 가까운 엣지 위치에서 콘텐츠를 캐싱하여 제공합니다. 
```
                        +---------------+
                        |  사용자 요청  |
                        +---------------+
                                    |
                                    |
                                    v
                        +---------------+
                        | CloudFront 엣지 |
                        |  캐싱 및 제공   |
                        +---------------+
                                    |
                                    |
                                    v
                        +---------------+
                        |  AWS S3      |
                        |  정적 콘텐츠 저장  |
                        +---------------+
```

### 코드로 이해하기

```typescript
// AWS SDK를 사용해 S3에 콘텐츠 업로드
import * as AWS from 'aws-sdk';
const s3 = new AWS.S3({ region: 'ap-northeast-2' });
const params = {
  Bucket: 'my-bucket',
  Key: 'index.html',
  Body: '정적 콘텐츠',
};
s3.upload(params, (err, data) => {
  if (err) {
    console.log(err);
  } else {
    console.log(data);
  }
});
```

```typescript
// 잘못된 사용 예: 캐싱을 고려하지 않은 경우
// 올바른 사용 예: CloudFront 캐싱을 사용한 경우
const cloudFront = new AWS.CloudFront({ region: 'ap-northeast-2' });
const distributionId = 'my-distribution-id';
const params = {
  DistributionId: distributionId,
  MaxItems: 100,
};
cloudFront.listInvalidations(params, (err, data) => {
  if (err) {
    console.log(err);
  } else {
    console.log(data);
  }
});
```

### 비교 분석

| 구분 | S3만 사용 | CloudFront 사용 | S3 + CloudFront |
|------|---------|---------------|----------------|
| 성능 | 중     | 높           | 최상        |
| 보안 | 중     | 높           | 최상        |
| 비용 | 중     | 높           | 합리적      |

### 실전 팁
- Best Practice: CloudFront의 엣지 위치를 최대한 활용하여 캐싱을 효율적으로 사용합니다.
- 흔한 실수와 해결법: 캐싱이 제대로 작동하지 않는 경우, CloudFront의 캐싱 설정을 확인합니다.
- 성능 관련 주의사항: 큰 파일의 경우, 부분전송을 사용하여 성능을 개선합니다.

### 한 줄 정리
AWS S3와 CloudFront를 함께 사용하여 정적 웹 호스팅의 성능과 보안을 최적화할 수 있습니다.