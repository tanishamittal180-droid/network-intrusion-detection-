# Safe Demo Runbook

1. Generate 5,000 synthetic records.
2. Train the optional model and record its actual metrics.
3. Start FastAPI and open `/docs`.
4. Start React with Vite.
5. Run the synthetic simulator in mixed mode.
6. For an abnormal demo, POST a synthetic flow with high connection_count and failed_connection_count to `/api/flows`.
7. Confirm the response contains matched rules, anomaly score, classification and alert.
8. Open the dashboard and refresh.
9. Open the alert through the API docs, change status to `INVESTIGATING`, add a note, then set `RESOLVED` or `FALSE_POSITIVE`.

No packet is transmitted by this project.
