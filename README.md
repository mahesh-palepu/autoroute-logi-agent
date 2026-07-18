# AutoRoute Dynamic Logi-Agent Panel 📦

An intelligent, state-driven inventory management and logistics parsing engine built with Python and Streamlit. This application simulates an automated enterprise supply chain system that processes inbound communications, mitigates stock shortages, enforces data security, and handles day-to-day warehouse accounting.

---

## 🚀 Operations & Core Features

* **Enterprise Setup Gateway:** A secure initialization portal to set up corporate profiles, product catalogs, registered supplier networks, and compliant backup vendors.
* **Dynamic Registry Expansion:** Allows administrators to add new product SKUs and register new supplier profiles on the fly without erasing or resetting existing session data.
* **Authorized Email Gatekeeper:** A security filter that verifies inbound message addresses against the registered supplier database. Messages from unrecognized senders trigger a **Critical Protocol Screen** for manager review.
* **AI-Powered Logistics Parsing:** A simulated natural language processing pipeline that scans message bodies to identify target products, dispatch nodes, and arrival delay timelines.
* **Automated Runway Calculation:** Compares current stock levels against historical daily sales velocity to determine if an identified transit delay will cause a stockout.
* **Multi-State Escalation Framework:** 
    * *State 4 (Ghost Data):* Locks the system if logs disconnect, requiring a manager concurrency token to force a manual sync.
    * *State 4 (Anomaly Velocity):* Catches sales spikes greater than 300% of the baseline and prompts the operator to classify them as an outlier or the "new normal."
    * *State 5 (Human Approval Queue):* Reroutes shortfalls to pre-vetted backup vendors or blocks orders if predatory pricing is detected.
* **Day Cycle Control & EOD Snapshot Matrix:** Simulates passing a business day, automatically deducts daily demand, and saves a snapshot log showing opening stock, units sold, and ending balances.
* **System Audit Ledger (Log Book):** An immutable historical timeline that logs all background security actions, system state mutations, and manual overrides.

---

## 📊 System Flowchart

This flowchart outlines the operational architecture of the AutoRoute engine. GitHub renders this diagram automatically using its native Mermaid support.

```mermaid
graph TD
    A[Start: Launch Application] --> B{Is Engine Onboarded?}
    B -- No --> C[Enterprise Setup Gateway]
    C --> D[Initialize Company, SKUs, & Suppliers]
    D --> E[Set Session State to Onboarded]
    E --> F[Load Main Panel Dashboard]
    B -- Yes --> F
    
    F --> G[Inbound Logistics Data Gateway]
    G --> H{Is Sender Email Authorized?}
    
    H -- No --> I[Engage Security Protocol: State Alert]
    I --> J{Manager Action?}
    J -- Reject & Purge --> F
    J -- Bypas & Run AI --> K[Execute AI Parsing Pipeline]
    
    H -- Yes --> K
    K --> L{SKU Identified?}
    L -- No --> M[Log Identification Deficit Error] --> F
    L -- Yes --> N{Does Stock Runway Cover Delay?}
    
    N -- Yes --> O[Log Low Risk & Maintain IDLE State] --> F
    N -- No --> P[Trigger State 5: Human Approval Queue]
    
    P --> Q{Evaluate Backup Vendor Status}
    Q -- Premium / Valid Margin --> R[One-Click Order: Replenish Stock] --> F
    Q -- Predatory Pricing / Risk --> S[Emergency Shutdown Broadcast] --> F
    
    F --> T[Sidebar Actions]
    T --> U[Manual Adjustments: Add / Deduct Stock] --> F
    T --> V[Dynamic Registry Expansion: Add SKU / Supplier] --> F
    T --> W[Close Today & Advance to Tomorrow] --> X[Calculate & Deduct Baseline Daily Sales]
    X --> Y[Generate Persistent EOD Snapshot Ledger] --> F
