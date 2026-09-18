# Queue backlog runbook

1. Check consumer health, delivery rate, and oldest-message age.
2. Confirm downstream dependencies are accepting traffic.
3. Scale consumers only after ruling out poison messages.
4. Never purge a queue without incident-lead approval.
