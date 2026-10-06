# 🛡️ Network Intrusion Detection System (IDS)

A practical **Network Intrusion Detection System (IDS)** designed to analyze network traffic and security logs, detect suspicious or malicious activities using **machine learning and rule-based detection**, and present security alerts through an interactive dashboard.

---

## 📌 Project Overview

The **Network Intrusion Detection System** is a cybersecurity project developed to demonstrate how modern security monitoring systems can identify potentially malicious network behavior.

The system analyzes network traffic/log data and classifies activities into different risk categories. It combines:

* 🤖 Machine Learning
* 🔍 Rule-Based Detection
* 📊 Traffic Analysis
* 🚨 Security Alerts
* 📈 Risk Scoring
* 🖥️ Interactive Dashboard
* 📋 Attack Classification
* 📑 Security Reports

The project is intended for **educational, research, and authorized defensive-security use**.

---

## 🎯 Objectives

The main objectives of this project are:

1. Detect suspicious network activities.
2. Identify common network attack patterns.
3. Apply machine learning to intrusion detection.
4. Combine ML detection with rule-based security signatures.
5. Calculate a risk score for detected activities.
6. Classify network events according to their severity.
7. Provide SOC-style security alerts.
8. Visualize network security information through a dashboard.
9. Generate useful security reports.
10. Improve understanding of practical intrusion detection systems.

---

# 🚀 Key Features

## 1. 🔍 Network Traffic Analysis

The system analyzes network traffic and extracts important features such as:

* Source IP
* Destination IP
* Source Port
* Destination Port
* Protocol
* Packet Count
* Byte Count
* Connection Duration
* Request Frequency
* Traffic Volume
* Connection State

These features are used to identify unusual behavior.

---

## 2. 🤖 Machine Learning Detection

The IDS can use machine-learning models to classify network activity.

Possible models include:

* Random Forest
* Decision Tree
* Logistic Regression
* Support Vector Machine
* K-Nearest Neighbors
* Neural Networks

The trained model can classify traffic as:

```text
Normal
Suspicious
Malicious
```

---

## 3. 🚨 Rule-Based Detection

In addition to machine learning, the system can use predefined security rules.

Example detection rules:

```text
Multiple failed connections
Port scanning behavior
Unusual traffic volume
Repeated connection attempts
Suspicious protocol activity
Abnormal packet frequency
```

This provides an additional detection layer.

---

# 🛡️ Attack Detection

The system can be designed to detect common categories of network attacks.

### 🔴 DoS / DDoS

Detects unusually high traffic or connection rates.

### 🔴 Port Scanning

Identifies repeated attempts to connect to multiple ports.

### 🔴 Brute Force

Detects repeated authentication or connection attempts.

### 🔴 Network Probing

Identifies suspicious reconnaissance behavior.

### 🔴 Suspicious Traffic

Detects traffic that differs significantly from normal network behavior.

### 🟢 Normal Traffic

Legitimate network activity is classified as normal.

---

# 📊 Risk Scoring

Each detected event can receive a risk score.

Example:

| Risk Score | Severity    |
| ---------: | ----------- |
|       0–20 | 🟢 Low      |
|      21–40 | 🟡 Medium   |
|      41–70 | 🟠 High     |
|     71–100 | 🔴 Critical |

The risk score can consider factors such as:

* Attack type
* Traffic frequency
* Number of connections
* Source reputation
* Protocol
* Anomaly level
* ML confidence
* Rule matches

---

# 🚨 Security Alert System

When suspicious traffic is detected, the system generates an alert.

Example:

```text
ALERT

Attack Type: Port Scan
Source IP: 192.168.1.25
Destination: 192.168.1.10
Severity: HIGH
Risk Score: 78
Detection Method: Rule-Based
Status: Investigate
```

Alerts can contain:

* Alert ID
* Timestamp
* Source IP
* Destination IP
* Attack type
* Severity
* Risk score
* Detection method
* Description
* Recommended action

---

# 📈 Dashboard

The project includes an interactive dashboard for security monitoring.

The dashboard can display:

### 📊 Network Statistics

* Total traffic
* Total connections
* Normal traffic
* Suspicious traffic
* Malicious traffic

### 🚨 Security Statistics

* Total alerts
* Critical alerts
* High-risk alerts
* Medium-risk alerts
* Low-risk alerts

### 📌 Attack Distribution

Example:

```text
DoS             █████████████
Port Scan       ████████
Brute Force     █████
Normal Traffic  █████████████████
```

### 📈 Additional Visualizations

* Traffic over time
* Attack distribution
* Severity distribution
* Top source IPs
* Top destination ports
* Protocol distribution
* Detection-method statistics

---

# 🧠 Detection Architecture

```text
                 Network Traffic / Logs
                          │
                          ▼
                 ┌─────────────────┐
                 │ Data Collection │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │ Data Processing │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │ Feature         │
                 │ Extraction      │
                 └────────┬────────┘
                          │
             ┌────────────┴────────────┐
             ▼                         ▼
     ┌────────────────┐       ┌────────────────┐
     │ Machine        │       │ Rule-Based     │
     │ Learning       │       │ Detection      │
     └────────┬───────┘       └────────┬───────┘
              │                        │
              └───────────┬────────────┘
                          ▼
                 ┌─────────────────┐
                 │ Risk Assessment │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │ Alert Generation│
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │ Security        │
                 │ Dashboard       │
                 └─────────────────┘
```

---

# 🏗️ System Architecture

```text
┌──────────────────────────────┐
│        Data Sources          │
│                              │
│ PCAP / CSV / Network Logs    │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│     Preprocessing Layer      │
│                              │
│ Cleaning / Encoding / Scaling│
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│      Detection Engine        │
│                              │
│ ML + Signature Rules         │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│       Risk Engine            │
│                              │
│ Score + Severity             │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│       Alert Manager          │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│      Web Dashboard           │
└──────────────────────────────┘
```

---

# 🧰 Technology Stack

## Backend

* Python
* Flask / FastAPI

## Machine Learning

* Scikit-learn
* NumPy
* Pandas

## Data Processing

* Pandas
* NumPy
* StandardScaler
* Label Encoding

## Frontend

Depending on implementation:

* HTML
* CSS
* JavaScript
* React

## Visualization

* Chart.js
* Matplotlib
* Plotly

## Database

Possible options:

* SQLite
* PostgreSQL
* MongoDB

---

# 📂 Project Structure

A recommended structure is:

```text
network-intrusion-detection/
│
├── backend/
│   ├── app.py
│   ├── routes/
│   ├── services/
│   ├── detection/
│   ├── models/
│   └── database/
│
├── frontend/
│   ├── src/
│   ├── components/
│   ├── pages/
│   └── assets/
│
├── ml/
│   ├── train.py
│   ├── predict.py
│   ├── preprocess.py
│   └── model.pkl
│
├── data/
│   ├── sample_traffic.csv
│   └── test_data.csv
│
├── reports/
│
├── screenshots/
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone <repository-url>
cd network-intrusion-detection
```

---

## 2. Create Virtual Environment

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Running the Backend

Example:

```bash
python backend/app.py
```

The backend may run at:

```text
http://127.0.0.1:5000
```

---

# ▶️ Running the Frontend

If using React:

```bash
cd frontend
npm install
npm run dev
```

The frontend will normally be available through the development server URL shown in the terminal.

---

# 🤖 Machine Learning Workflow

The ML pipeline follows:

```text
Dataset
   ↓
Data Cleaning
   ↓
Feature Selection
   ↓
Encoding
   ↓
Feature Scaling
   ↓
Train/Test Split
   ↓
Model Training
   ↓
Model Evaluation
   ↓
Model Saving
   ↓
Prediction
```

---

# 📚 Dataset

The system can be tested using publicly available cybersecurity datasets or safely generated/synthetic traffic data.

Possible datasets include:

* CICIDS2017
* UNSW-NB15
* NSL-KDD
* Custom synthetic network traffic

Dataset selection depends on the ML experiment and project requirements.

---

# 🧪 Testing

The system should be tested using different traffic categories.

Example:

| Test Case                 | Expected Result    |
| ------------------------- | ------------------ |
| Normal HTTP traffic       | Normal             |
| High connection rate      | Suspicious         |
| Multiple port connections | Port Scan          |
| Repeated login attempts   | Brute Force        |
| Extremely high traffic    | DoS/DDoS indicator |
| Unknown abnormal pattern  | Suspicious         |

Testing should preferably use **synthetic, benchmark, or authorized traffic** rather than unauthorized live traffic.

---

# 🔌 Example API Endpoints

A REST API implementation may include:

### Health Check

```http
GET /api/health
```

### Traffic Analysis

```http
POST /api/analyze
```

### Get Alerts

```http
GET /api/alerts
```

### Get Statistics

```http
GET /api/statistics
```

### Get Detection Details

```http
GET /api/detection/<id>
```

### Generate Report

```http
GET /api/report
```

---

# 📋 Example Detection Report

```text
====================================
NETWORK SECURITY ALERT
====================================

Alert ID       : IDS-00021
Timestamp      : 2026-10-06 15:30:22

Source IP      : 192.168.1.25
Destination IP : 192.168.1.10

Protocol       : TCP
Source Port    : 49152
Destination    : Multiple Ports

Attack Type    : Port Scan

Risk Score     : 82/100
Severity       : HIGH

Detection      : Rule + ML

Recommendation:
Investigate the source host and review
recent connection attempts.
====================================
```

---

# 📊 Model Evaluation

Machine-learning performance can be evaluated using:

* Accuracy
* Precision
* Recall
* F1-Score
* Confusion Matrix
* ROC-AUC
* False Positive Rate
* False Negative Rate

Example:

```text
Accuracy  : 95%
Precision : 94%
Recall    : 93%
F1-Score  : 93.5%
```

> The actual values depend on the dataset, preprocessing pipeline, model, and train/test split. Do not use example values as measured results unless they were actually obtained.

---

# 🔐 Security Considerations

The project follows defensive-security principles.

### Data Protection

Avoid collecting unnecessary sensitive network information.

### No Unauthorized Monitoring

Only analyze traffic that you are authorized to inspect.

### Secure API

Production deployments should use:

* Authentication
* Authorization
* HTTPS
* Input validation
* Rate limiting
* Secure logging

### Sensitive Data

Avoid unnecessarily storing:

* Passwords
* Authentication tokens
* Private payload contents
* Personal information

---

# ⚠️ Limitations

The system may have limitations such as:

* False positives
* False negatives
* Dataset bias
* Limited attack coverage
* ML model dependency
* Changing network behavior
* Encrypted traffic visibility limitations

An IDS should therefore be treated as a **security-assistance system**, not an absolute source of truth.

---

# 🚀 Future Enhancements

Future versions can include:

* 🔥 Real-time packet capture
* 🤖 Deep-learning-based detection
* 🧠 Automated anomaly detection
* 🌐 IP reputation integration
* 📡 Live network monitoring
* 🔔 Email/SMS security alerts
* 📊 Advanced SOC dashboard
* 📑 Automated PDF reports
* 🗺️ Attack-source visualization
* 🔐 Role-based authentication
* 🧩 SIEM integration
* 🐳 Docker deployment
* ☁️ Cloud deployment
* 📈 Long-term security analytics

---

# 🎓 Learning Outcomes

Through this project, the following concepts can be learned:

### Cybersecurity

* Network security
* Intrusion detection
* Threat detection
* Security monitoring
* Incident analysis

### Machine Learning

* Data preprocessing
* Feature engineering
* Classification
* Model training
* Model evaluation

### Software Development

* REST APIs
* Backend development
* Frontend dashboards
* Database integration
* System architecture

### SOC Concepts

* Alert generation
* Risk classification
* Security triage
* Detection rules
* Incident investigation

---

# 🛡️ IDS Workflow

The overall workflow is:

```text
Network Data
     ↓
Collection
     ↓
Preprocessing
     ↓
Feature Extraction
     ↓
ML Detection + Rule Detection
     ↓
Risk Scoring
     ↓
Alert Generation
     ↓
Security Investigation
     ↓
Response
```

---

# 💡 Project Philosophy

> **Detect early. Analyze carefully. Respond safely.**

An effective intrusion detection system should not simply generate thousands of alerts. It should help security teams identify **meaningful threats, prioritize risks, and investigate suspicious behavior efficiently.**

---
# screenshot 
<img width="1364" height="639" alt="Screenshot 2026-10-03 013417" src="https://github.com/user-attachments/assets/2028494a-2f40-440e-b4e2-b5a3f89cc283" />
<img width="1343" height="425" alt="Screenshot 2026-10-03 013437" src="https://github.com/user-attachments/assets/7016ab91-8127-4557-b9f6-184ce6e4fca8" />
<img width="911" height="409" alt="Screenshot 2026-10-03 013448" src="https://github.com/user-attachments/assets/7baddb20-1570-4d6c-bdce-26bcf0ee9d0b" />
<img width="1346" height="632" alt="Screenshot 2026-10-03 013504" src="https://github.com/user-attachments/assets/3238fdda-8422-42e5-9827-479a3a416e4d" />


# 👩‍💻 Educational Purpose

This project is developed for:

* Academic projects
* Cybersecurity learning
* Machine-learning experimentation
* Network-security research
* SOC simulation
* Defensive-security training

Use only **authorized, synthetic, benchmark, or laboratory network data** when testing the system.

---

# 📜 License

This project can be released under the **MIT License** or another license appropriate to the project.

---

# ⭐ Acknowledgement

This project demonstrates the integration of:

**Cybersecurity + Machine Learning + Network Analysis + Web Development + Security Monitoring**

It is designed as a learning platform for understanding how modern **Network Intrusion Detection Systems** can detect, classify, and prioritize suspicious network activity.
