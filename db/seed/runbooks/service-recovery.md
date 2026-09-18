# Service recovery runbook

1. Capture error rate, latency, saturation, and the last deployment.
2. Validate health checks and dependency reachability.
3. Prefer rollback over manual container mutation.
4. Use automation only from the explicit whitelist and retain its audit record.
