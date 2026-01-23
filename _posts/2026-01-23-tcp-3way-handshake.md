---
title: "TCP 3-Way Handshake"
date: 2026-01-23 12:00:00 +0900
categories: [개발노트]
tags: [Network, TCP, Protocol]
---

> TCP 연결 수립을 위한 핵심 메커니즘

## 개요

```
Client          Server
  │── SYN ────────→│   (seq=x)
  │←── SYN-ACK ────│   (seq=y, ack=x+1)
  │── ACK ────────→│   (ack=y+1)
```

---

## 각 단계 상세

### 1단계: SYN (Synchronize)

```
Client ──── SYN ────→ Server
         seq=1000
```

| 항목 | 설명 |
|------|------|
| 목적 | 클라이언트가 연결 요청 |
| seq=1000 | 클라이언트의 초기 시퀀스 번호 (ISN: Initial Sequence Number) |
| ISN 생성 | 보안상 랜덤 생성 (예측 공격 방지) |
| 플래그 | SYN = 1 |

### 2단계: SYN-ACK

```
Client ←── SYN-ACK ── Server
         seq=2000
         ack=1001
```

| 항목 | 설명 |
|------|------|
| 목적 | 서버가 요청 수락 + 자신도 연결 요청 |
| seq=2000 | 서버의 초기 시퀀스 번호 |
| ack=1001 | "클라이언트의 1000번까지 받았고, 1001번 기다림" |
| 플래그 | SYN = 1, ACK = 1 |

### 3단계: ACK

```
Client ──── ACK ────→ Server
         seq=1001
         ack=2001
```

| 항목 | 설명 |
|------|------|
| 목적 | 클라이언트가 서버 요청 수락 확인 |
| ack=2001 | "서버의 2000번까지 받았고, 2001번 기다림" |
| 결과 | 양방향 통신 가능 (ESTABLISHED 상태) |

---

## 왜 3-Way인가?

### 2-Way일 경우 문제점

```
문제 시나리오:

Client ── SYN ──→ Server     (지연됨)
Client ── SYN ──→ Server     (재전송, 먼저 도착)
Client ←─ ACK ─── Server     (연결 수립)
      ... 통신 후 종료 ...
Client ←─ ACK ─── Server     (지연된 SYN에 대한 응답!)
                              → 유령 연결 발생!
```

### 3-Way의 장점

**양측 모두 송수신 능력을 확인:**

| 단계 | 확인 내용 |
|------|----------|
| 1단계 | 클라이언트 → 서버 (클라이언트 송신 OK) |
| 2단계 | 서버 → 클라이언트 (서버 송수신 OK) |
| 3단계 | 클라이언트 → 서버 (클라이언트 수신 OK) |

---

## 시퀀스 번호의 역할

### 데이터 전송 예시

```
Client ── seq=1001, data="Hello" (5 bytes) ──→ Server
Client ←── ack=1006 ─────────────────────── Server
           (1001 + 5 = 1006, 다음 바이트 요청)
```

### 시퀀스 번호의 기능

| 기능 | 설명 |
|------|------|
| 순서 보장 | 패킷이 뒤섞여 도착해도 재조립 가능 |
| 중복 감지 | 같은 seq면 중복 패킷으로 판단 |
| 손실 감지 | ack가 안 오면 재전송 |

---

## 실제 패킷 (Wireshark)

### 1단계 SYN

```
Flags: 0x002 (SYN)
Sequence number: 0 (relative)
Window size: 65535
Options: MSS=1460, SACK, WScale=6
```

### 2단계 SYN-ACK

```
Flags: 0x012 (SYN, ACK)
Sequence number: 0 (relative)
Acknowledgment number: 1
Options: MSS=1460, SACK, WScale=6
```

### 3단계 ACK

```
Flags: 0x010 (ACK)
Sequence number: 1
Acknowledgment number: 1
```

---

## 연결 종료: 4-Way Handshake

```
Client          Server
  │── FIN ────────→│   (연결 종료 요청)
  │←── ACK ────────│   (확인)
  │←── FIN ────────│   (서버도 종료 요청)
  │── ACK ────────→│   (확인)
```

### 왜 4-Way인가?

- 서버가 아직 보낼 데이터가 남아있을 수 있음
- ACK와 FIN을 분리해서 **Half-Close** 지원
- 한쪽이 먼저 종료해도 다른 쪽은 계속 데이터 전송 가능

---

## 보안 이슈

### SYN Flood 공격

```
Attacker ── SYN (spoofed IP) ──→ Server
Attacker ── SYN (spoofed IP) ──→ Server
Attacker ── SYN (spoofed IP) ──→ Server
... 수천 개 ...

Server: SYN-ACK를 가짜 IP로 보냄 → 응답 없음
        → 연결 대기 큐(backlog) 가득 참
        → 정상 연결 불가 (DoS)
```

### 방어 방법

| 방법 | 설명 |
|------|------|
| SYN Cookies | 상태를 저장하지 않고 암호화된 쿠키로 검증 |
| Rate Limiting | IP당 SYN 요청 수 제한 |
| Firewall | 비정상 패턴 탐지 및 차단 |
| Backlog 증가 | 대기 큐 크기 늘리기 (임시방편) |

---

## TCP 상태 전이

```
CLOSED
   │
   │ (active open, send SYN)
   ▼
SYN_SENT ──────────────────────┐
   │                           │
   │ (receive SYN-ACK,         │ (receive SYN,
   │  send ACK)                │  send SYN-ACK)
   ▼                           ▼
ESTABLISHED              SYN_RECEIVED
                               │
                               │ (receive ACK)
                               ▼
                          ESTABLISHED
```

---

## 참고 자료

- [RFC 793 - Transmission Control Protocol](https://tools.ietf.org/html/rfc793)
- [RFC 7413 - TCP Fast Open](https://tools.ietf.org/html/rfc7413)
