# Chapter 0: Production Architecture & Local Bootstrap

## System Blueprint
Our FinTech engine operates on a polyglot microservice pattern:
1. **Auth Service (Go):** Handles low-latency JWT validation and probe monitoring.
2. **Ledger Service (Python/FastAPI):** Enforces transaction domain rules and persistence.
3. **Notification Service (Go):** Asynchronous webhook runner for high-throughput alert dispatching.

```
                  [ Docker Compose Bridge Network ]
                                 │
     ┌───────────────────────────┼───────────────────────────┐
     ▼                           ▼                           ▼
[ Auth Service ]        [ Ledger Service ]      [ Notification Service ]
  (Go @ 8080)            (FastAPI @ 8081)             (Go @ 8082)
```

## Local Verification Commands

To verify full system orchestration locally:

```bash
docker compose up -d --build
docker compose ps
```

### Health Probe Output
```json
{"status":"HEALTHY","timestamp":"2026-10-12T06:17:14Z","service":"auth-service"}
{"status":"HEALTHY","timestamp":"2026-10-12T06:17:14Z","service":"ledger-service"}
{"status":"HEALTHY","timestamp":"2026-10-12T06:17:14Z","service":"notification-service"}
```
