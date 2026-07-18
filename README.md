# 📦 AutoRoute Logi-Agent

### 🚀 FlowZint AI Hackathon 2026 Submission (Category: Open Innovation)

An intelligent, dynamic supply chain orchestration system built to protect regional logistics networks from communication disruptions and data anomalies.

## 🔍 The Problem It Solves
1. **Unstructured Chaos:** Logistics teams waste hours reading disorganized supplier emails to figure out transit delays.
2. **Brittle Data Syncs ("Ghost Data"):** If a warehouse fails to upload its daily log, standard automated systems either crash or make incorrect blind orders.

## ✨ Key Features
- **Dynamic Corporate Gateway:** Secure onboarding that captures unique company profiles, emails, phone numbers, and any number of suppliers.
- **AI Text Parsing Engine:** Extracts real-time arrival delays directly from raw email text (converting hours or days dynamically) to instantly calculate stock runway shortages.
- **Smart Mitigation Workflow:** Automatically flags the responsible supplier, drafts contract breach notifications, and calculates exact spot-market purchase quantities to prevent stockouts.
- **Operational Circuit Breaker:** Instantly freezes automated processes and locks inputs if daily warehouse sync logs are missing, ensuring high-availability data safety.

## 🛠️ Tech Stack & How to Run
Built using **Python** and **Streamlit**.

1. Install requirements:
   ```bash
   pip install streamlit pandas
