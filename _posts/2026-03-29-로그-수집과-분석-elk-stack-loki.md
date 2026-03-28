---
title: "[Deep Dive] 로그 수집과 분석 (ELK Stack, Loki)"
date: 2026-03-29 08:10:13 +0900
categories: [개발뉴스]
tags: [CS, 심화]
---

## 표면적 이해
로그 수집과 분석은 어플리케이션의 성능과 문제를 파악하기 위해 로그 데이터를 수집하고 분석하는 것을 말한다.

## Deep Dive

### 왜 필요한가?
- 로그 수집과 분석은 어플리케이션의 오류와 성능 저하를 파악하고 개선하는 데하다. 이전 방식의 로그 수집은 파일을 수동으로 확인하거나, 로그 데이터를 중앙화된 저장소에 모아두었다. 그러나 이러한 방식은 데이터의 양이 많아질수록 효율적이지 못하고, 데이터를 분석하고 시각화하기 어려웠다.

### 내부 동작 원리
- 로그 수집과 분석을 위한 ELK Stack과 Loki는 다음과 같은 구조로 작동한다.
```
         +---------------+
         |  로그 발생  |
         +---------------+
                  |
                  |
                  v
         +---------------+
         | 로그 수집기   |
         |  (Filebeat,    |
         |   Vector)     |
         +---------------+
                  |
                  |
                  v
         +---------------+
         | 로그 전송기   |
         |  (Logstash,    |
         |   Vector)     |
         +---------------+
                  |
                  |
                  v
         +---------------+
         | 로그 저장소  |
         |  (Elasticsearch,|
         |   Loki)       |
         +---------------+
                  |
                  |
                  v
         +---------------+
         | 로그 분석도구  |
         |  (Kibana,      |
         |   Grafana)    |
         +---------------+
```
- ELK Stack은 Filebeat, Logstash, Elasticsearch, Kibana로 구성되며, Loki는 Vector와 Grafana를 사용한다.

### 코드로 이해하기

```typescript
// 로그 수집기 설정 예 (Filebeat)
const filebeatConfig = {
  inputs: [
    {
      type: 'log',
      enabled: true,
      paths: ['/path/to/log/file.log'],
    },
  ],
  output: {
    elasticsearch: {
      hosts: ['http://elasticsearch:9200'],
    },
  },
};
```

```typescript
// 로그 전송기 설정 예 (Logstash)
const logstashConfig = {
  input: {
    beats: {
      port: 5044,
    },
  },
  filter: {
    grok: {
      match: {
        message: '%{HTTPDATE:timestamp} %{IP:client_ip} - - %{WORD:http_method} %{URIPATH:request_uri} HTTP/%{NUMBER:http_version} %{NUMBER:status_code} %{NUMBER:body_bytes_sent}',
      },
    },
  },
  output: {
    elasticsearch: {
      hosts: ['http://elasticsearch:9200'],
      index: 'logs-%{+YYYY.MM.dd}',
    },
  },
};
```

### 비교 분석

| 구분 | ELK Stack | Loki |
|------|---|---|
| 로그 수집기 | Filebeat | Vector |
| 로그 전송기 | Logstash | Vector |
| 로그 저장소 | Elasticsearch | Loki |
| 로그 분석도구 | Kibana | Grafana |

### 실전 팁
- 로그 수집과 분석을 위해 로그 형식을 일관되게 유지하는 것이 중요하다.
- 로그 데이터를 효율적으로 저장하고 분석하기 위해 인덱싱과 파티셔닝을 고려해야 한다.
- 로그 분석을 위해 다양한 시각화 도구와 플러그인을 사용하면 효과적인 결과를 얻을 수 있다.

### 한 줄 정리
로그 수집과 분석은 어플리케이션의 성능과 문제를 파악하고 개선하기 위해 로그 데이터를 수집하고 분석하는 것을 말하며, ELK Stack과 Loki는 각각의 장단점이 있다.