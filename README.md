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

## 🧮 Core Algorithm Matrix

* **Ingestion & Security Verification:** Validates the sender's email against the authorized supplier registry before allowing any data extraction to protect the engine from unverified external inputs.
* **Entity & Delay Extraction:** Scans the incoming message text using regular expressions to isolate product names and calculate delay timelines from hours or days into standard day units.
* **Runway Deficit Assessment:** Divides current warehouse stock by the historical daily sales average to determine the inventory runway, flagging an exception if the parsed delay exceeds the available buffer.
* **Dynamic State Mutation:** Shifts the core system state automatically from idle to a dedicated approval queue the exact moment a supply gap or operational anomaly is detected.
* **End-of-Day Ledger Accounting:** Deducts baseline consumer demand from live stock counts at the close of each day, caps balances at zero to prevent negative values, and commits the metrics to history.

---

## 📝 Conclusion

* **Functional Prototype Success:** Proves that a state-driven dashboard can handle complex supply chain challenges like automated message parsing and rule-based inventory routing.
* **Operational Efficiency Gains:** Removes human calculation errors by processing stock runways automatically and instantly alerting teams to upcoming shortages.
* **Proactive Security Foundation:** Combines strict sender filtering with automated anomaly checks to keep corporate supply data secure and reliable.

---

## 🛠️ Next Steps: Building a Real Working Production Prototype

* **Production AI Model Integration:** Replaces basic keyword matching with a dedicated large language model API (like OpenAI or Anthropic) to interpret messy, unstructured emails cleanly.
* **Persistent Database Storage:** Migrates data out of temporary app memory into a live database like PostgreSQL or Supabase to protect records and handle multiple users safely.
* **Automated Inbox Webhooks:** Integrates the application directly with actual business email accounts using tools like SendGrid to ingest supply alerts automatically without copy-pasting.
* **Role-Based Access Control:** Implements secure logins and user permissions so warehouse teams can update stock while restricting order approvals to managers.

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

