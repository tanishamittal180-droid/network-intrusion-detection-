# 10 Interview Questions and Answers

1. **Explain your project.** — I built a defensive Network IDS simulation that analyzes synthetic network-flow data. It extracts rates, connection and failure features, applies explainable signatures and statistical anomaly detection, optionally uses Random Forest, combines signals into a risk score, stores alerts in SQLite, and presents them in a SOC dashboard. I deliberately avoided generating real attack traffic.

2. **What is an IDS and how is it different from IPS?** — An IDS detects and alerts; an IPS can additionally take configured preventive action. My project is an IDS simulation because its purpose is detection, triage, and investigation.

3. **Signature vs anomaly detection?** — Signatures compare activity with predefined patterns. Anomaly detection compares activity with a normal baseline. Signatures are explainable but can miss new patterns; anomalies can find unusual behavior but may create false positives.

4. **Which features did you engineer?** — Packet/byte counts, duration, bytes/sec, packets/sec, connection rate, failure ratio, SYN ratio, average packet size, and destination-port diversity. They convert traffic behavior into measurable values.

5. **How does anomaly scoring work?** — I fit robust baseline statistics on normal flow features and measure deviations for new flows. The deviations are normalized into a 0–100 score. An anomaly means unusual behavior, not automatically malicious behavior.

6. **How is risk calculated?** — Rule matches, anomaly score, and optional ML probability are combined with configurable weights. The result is bounded to 0–100 and mapped to a project classification threshold.

7. **What are false positives and false negatives?** — A false positive flags legitimate activity; a false negative misses suspicious activity. I would reduce them through better baselines, contextual enrichment, threshold tuning, correlation, and analyst feedback.

8. **Why Random Forest?** — It is a strong interpretable baseline for tabular flow features, handles nonlinear relationships, and needs relatively little preprocessing. I still evaluate it with precision, recall, F1 and a confusion matrix.

9. **How did you test safely?** — All attack-like behavior is represented as synthetic records. I test normal protocols, high connection rates, repeated failures, multi-port patterns, SYN-heavy statistics, high volume, invalid input, feature calculations, rules, anomaly scores, alerts, APIs, and dashboard data.

10. **How would you improve it for a real SOC?** — I would ingest authorized NetFlow/Zeek/Suricata telemetry, add authentication/RBAC, forward JSON alerts to a SIEM, enrich events with approved asset context, improve correlation and baselines, and monitor model drift.
