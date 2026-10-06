# Project Report — Network Intrusion Detection System (IDS) Simulation

## Abstract
This project implements a safe, modular Network Intrusion Detection System simulation. Synthetic flow records represent normal and suspicious statistical patterns. A feature extractor computes traffic rates and ratios; a signature engine detects configured patterns; a statistical detector measures deviation from a normal baseline; an optional Random Forest model provides supervised classification; and a risk engine combines signals into an explainable score. FastAPI exposes the detection service and SQLite stores flows, alerts, rules, and analyst notes. A React dashboard presents SOC-style metrics.

## Introduction
Organizations monitor network telemetry to identify events that may require investigation. An IDS detects and reports potentially suspicious behavior without automatically blocking it. This project intentionally focuses on detection and analyst workflow.

## Objectives
Generate safe synthetic traffic, engineer network features, implement signatures and anomaly detection, optionally evaluate ML, score risk, create/correlate alerts, store evidence, and visualize activity.

## Proposed System
Synthetic Generator → API → Feature Extraction → Rule/Anomaly/ML → Risk → Alert → Database → Dashboard.

## Detection Methods
Signature detection is explainable and fast for known patterns. Anomaly detection identifies deviations from baseline but may produce false positives. Hybrid detection combines these signals.

## Machine Learning
Random Forest is trained on a held-out split of the generated dataset. Evaluation includes accuracy, precision, recall, F1, and a confusion matrix. Results are generated at runtime and should be reported exactly as printed by the training script.

## SOC Workflow
Network event → alert queue → triage → context → investigation → status update → documentation.

## Security and Privacy
Synthetic data avoids exposure of real traffic. Production deployments should authenticate analysts, authorize actions, encrypt transport, protect logs, use environment-based secrets, rate-limit APIs, sanitize UI output, and apply least privilege. Network telemetry may contain sensitive IPs, service metadata, and behavioral information.

## Limitations
The simulator does not capture packet payloads or real protocol semantics. Thresholds are educational assumptions. Synthetic labels can make ML performance easier than real-world detection. No result should be interpreted as proof of compromise.

## Future Scope
Authorized Zeek/Suricata/NetFlow ingestion, SIEM integration, stronger behavioral baselines, enrichment, streaming, RBAC, model drift monitoring, and scalable storage.

## Conclusion
The project demonstrates core defensive IDS concepts while remaining executable without a network lab or external targets.
