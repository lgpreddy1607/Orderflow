# Gunicorn Blocking Experiment

## Objective
Understand how Gunicorn sync workers handle concurrent requests and how worker count affects throughput.

## Setup

### Case 1 — Single Worker
- Workers: 1
- Artificial delay: 10 seconds (`time.sleep(10)`)
- Requests sent: 4 (near-simultaneous)

### Case 2 — Two Workers
- Workers: 2
- Artificial delay: 10 seconds (`time.sleep(10)`)
- Requests sent: 4 (near-simultaneous)

---

## Observations

### Case 1 — Single Worker
- Requests processed sequentially
- Completion times:
  - Req1 → ~10s
  - Req2 → ~20s
  - Req3 → ~30s
  - Req4 → ~40s

### Case 2 — Two Workers
- Requests processed in parallel batches
- Completion times:
  - Req1 & Req2 → ~10s
  - Req3 & Req4 → ~20s

---

## Conclusion

- Each sync worker handles only one request at a time
- Total concurrency = number of workers
- Additional requests are queued until a worker becomes available
- Latency increases linearly with queue depth

---

## Key Insight

Gunicorn sync workers are blocking.

System capacity is defined by:

> Workers / Request Latency

If incoming request rate exceeds this capacity:

- Requests queue up
- Latency increases
- System eventually becomes unstable under sustained load