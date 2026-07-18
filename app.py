import streamlit as st
import pandas as pd
import math
import time
import re
from datetime import datetime

# Page Configuration
st.set_page_config(page_title="AutoRoute Core Engine", layout="wide")

# ==============================================================================
# ENGINE UTILITIES & PARSER
# ==============================================================================
def validate_email_format(email_str):
    email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return bool(re.match(email_pattern, email_str))

def run_visual_ai_parsing_pipeline(text_content, product_list, supplier_list):
    """Scans text to isolate products, delay intervals, and matched suppliers."""
    matched_sku = None
    matched_supplier = None
    parsed_delay = 0.0
    
    for prod in product_list:
        if prod.lower() in text_content.lower():
            matched_sku = prod
            break
            
    for sup in supplier_list:
        if sup['name'].lower() in text_content.lower():
            matched_supplier = sup['name']
            break
            
    day_match = re.search(r"(\d+)\s*-?\s*day", text_content, re.IGNORECASE)
    hour_match = re.search(r"(\d+)\s*-?\s*hour", text_content, re.IGNORECASE)
    
    if day_match:
        parsed_delay = float(day_match.group(1))
    elif hour_match:
        parsed_delay = float(hour_match.group(1)) / 24.0
        
    return {
        "sku": matched_sku,
        "supplier": matched_supplier if matched_supplier else "Unregistered Node",
        "delay_days": parsed_delay
    }

def add_log_entry(action, details, status="SUCCESS"):
    """Appends an operational tracking event to the Log Book state."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.log_book.insert(0, {
        "Timestamp": timestamp,
        "Event Action": action,
        "System Details": details,
        "Status Gate": status
    })

# ==============================================================================
# STATE INITIALIZATION
# ==============================================================================
if 'onboarded' not in st.session_state:
    st.session_state.onboarded = False
if 'corp_details' not in st.session_state:
    st.session_state.corp_details = {}
if 'database' not in st.session_state:
    st.session_state.database = {}
if 'primary_suppliers' not in st.session_state:
    st.session_state.primary_suppliers = []
if 'backup_ledger' not in st.session_state:
    st.session_state.backup_ledger = []
if 'system_state' not in st.session_state:
    st.session_state.system_state = "IDLE"
if 'token_lock_holder' not in st.session_state:
    st.session_state.token_lock_holder = None
if 'active_exception' not in st.session_state:
    st.session_state.active_exception = None
if 'simulated_conflict' not in st.session_state:
    st.session_state.simulated_conflict = False
if 'log_book' not in st.session_state:
    st.session_state.log_book = []
if 'current_day' not in st.session_state:
    st.session_state.current_day = 1
if 'eod_snapshots' not in st.session_state:
    st.session_state.eod_snapshots = []

# ==============================================================================
# SCREEN A: ENTERPRISE SETUP GATEWAY
# ==============================================================================
if not st.session_state.onboarded:
    st.title("🏢 AutoRoute Enterprise Setup Gateway")
    st.markdown("### Initialize Custom Sourcing Architecture & Dynamic Product Matrix")
    st.markdown("---")
    
    with st.form("dynamic_matrix_setup"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🏢 1. Corporation Contact Profile")
            corp_name = st.text_input("Company / Entity Name", value="Apex Global Tech Distribution")
            reg_id = st.text_input("Business Registration / Tax ID", value="TAX-77-89412")
            email = st.text_input("Corporate Operations Email Address", value="supplychain@apexglobal.com")
            phone = st.text_input("Emergency Mobile Contact", value="+1 (555) 489-1212")
            region = st.selectbox("Active Logistics Zone", ["North America Core", "EMEA Operations", "APAC Network"])
            
            st.markdown("---")
            st.markdown("#### 🚚 2. Initial Supplier Network Registry")
            st.markdown("*Format: Company Name, Email, Phone Number*")
            supplier_raw = st.text_area(
                "Authorized Suppliers Ledger:",
                value="Prime Logistics Inc., dispatch@primelogistics.com, +1-555-0199\nNexus Manufacturing Group, orders@nexusmfg.com, +1-555-0288"
            )
            
        with col2:
            st.markdown("#### 📦 3. Dynamic Product Catalog & Inventory Setup")
            st.markdown("*Format: Product Name, Current Stock, Average Daily Sales*")
            products_raw = st.text_area(
                "Product Catalog Configuration Ledger Matrix:",
                value="Wireless Headphones, 500, 25\nSmart Watches, 320, 15\nRaw Coffee Beans, 800, 40"
            )
            
            st.markdown("---")
            st.markdown("#### 🛡️ 4. Pre-Vetted Backup Suppliers Ledger")
            b1_name = st.text_input("Backup Vendor 1 Name", "Premium Reserve Cultivators")
            b1_grade = st.selectbox("Backup 1 Quality Grade", ["Premium", "Standard"])
            b1_price = st.selectbox("Backup 1 Price Margin Assessment", ["Valid Margin", "Predatory Pricing"])
            
        st.markdown("---")
        compile_btn = st.form_submit_button("🚀 Compile Custom Operational Engine Layout")
        
        if compile_btn:
            if not corp_name or not products_raw or not supplier_raw:
                st.error("Setup Deficit: Ensure all mandatory sections are completed.")
            elif not validate_email_format(email):
                st.error("❌ Authentication Error: Invalid Corporate Email Address format.")
            else:
                # Parse baseline products
                parsed_db = {}
                for line in products_raw.split("\n"):
                    if "," in line:
                        parts = [p.strip() for p in line.split(",")]
                        if len(parts) == 3:
                            parsed_db[parts[0]] = {"stock": int(parts[1]), "history_avg": float(parts[2])}
                
                # Parse structured suppliers
                parsed_suppliers = []
                for line in supplier_raw.split("\n"):
                    if "," in line:
                        parts = [p.strip() for p in line.split(",")]
                        if len(parts) == 3:
                            parsed_suppliers.append({"name": parts[0], "email": parts[1], "phone": parts[2]})
                
                st.session_state.corp_details = {"name": corp_name, "reg_id": reg_id, "email": email, "phone": phone, "region": region}
                st.session_state.database = parsed_db
                st.session_state.primary_suppliers = parsed_suppliers
                st.session_state.backup_ledger = [{"name": b1_name, "grade": b1_grade, "price": b1_price}]
                st.session_state.current_day = 1
                st.session_state.onboarded = True
                
                add_log_entry("SYSTEM_INITIALIZATION", f"Compiled core architecture with {len(parsed_db)} SKUs and {len(parsed_suppliers)} authorized suppliers.")
                st.rerun()

# ==============================================================================
# SCREEN B: MULTI-TAB DASHBOARD ORCHESTRATOR
# ==============================================================================
else:
    product_list = list(st.session_state.database.keys())
    authorized_emails = [sup['email'] for sup in st.session_state.primary_suppliers]
    
    # Left Context Sidebar Elements
    with st.sidebar:
        st.title("🔒 Terminal Session Context")
        st.info(f"**🏢 Company:** {st.session_state.corp_details['name']}\n📅 **Calendar:** `Day {st.session_state.current_day}`")
        
        if st.button("🚪 Reset Framework & Clear Profile", use_container_width=True):
            st.session_state.onboarded = False
            st.session_state.database = {}
            st.session_state.primary_suppliers = []
            st.session_state.backup_ledger = []
            st.session_state.system_state = "IDLE"
            st.session_state.active_exception = None
            st.session_state.log_book = []
            st.session_state.eod_snapshots = []
            st.session_state.current_day = 1
            st.rerun()
            
        st.markdown("---")
        st.title("🗄️ Real-Time Integrity Sync")
        log_sync_success = st.checkbox("Synchronize Warehouse Logs Daily", value=True)
        
        # DAY CYCLE CONTROL MODULE
        st.markdown("---")
        st.markdown("### 📆 Day Cycle Control")
        if st.button("🌙 Close Today & Advance to Tomorrow", use_container_width=True):
            day_snapshot_records = []
            consumption_summary = []
            
            for prod in product_list:
                daily_demand = int(st.session_state.database[prod]["history_avg"])
                starting_stock = st.session_state.database[prod]["stock"]
                ending_stock = max(0, starting_stock - daily_demand)
                actual_sold = starting_stock - ending_stock
                
                # Update live database stock level
                st.session_state.database[prod]["stock"] = ending_stock
                consumption_summary.append(f"{prod} (-{actual_sold})")
                
                # Append to persistent EOD accounting snapshots list
                st.session_state.eod_snapshots.append({
                    "Operational Day": f"Day {st.session_state.current_day}",
                    "Product Item SKU": prod,
                    "Opening Starting Stock": starting_stock,
                    "Units Sold Out": actual_sold,
                    "Remaining Ending Balance": ending_stock
                })
            
            add_log_entry(f"DAY_{st.session_state.current_day}_CLOSED", f"Subtracted daily demand allocations: {', '.join(consumption_summary)}.")
            st.session_state.current_day += 1
            st.toast(f"Day closed. Advancing calendar state!", icon="🌤️")
            time.sleep(0.4)
            st.rerun()

        # NEW FEATURE: DYNAMIC REGISTRY EXPANSION (Add without data loss)
        st.markdown("---")
        with st.expander("➕ Expand Sourcing Registry Live", expanded=False):
            st.markdown("##### Add New Product Item")
            new_p_name = st.text_input("Product Name", key="new_p_name")
            new_p_stock = st.number_input("Starting Stock Level", min_value=0, value=100, key="new_p_stock")
            new_p_sales = st.number_input("Average Daily Sales", min_value=1, value=10, key="new_p_sales")
            
            if st.button("Save Product SKU"):
                if new_p_name and new_p_name not in st.session_state.database:
                    st.session_state.database[new_p_name] = {"stock": int(new_p_stock), "history_avg": float(new_p_sales)}
                    add_log_entry("REGISTRY_EXPANSION", f"Dynamically integrated new product item line: {new_p_name} without wiping system cache.")
                    st.toast(f"Added {new_p_name} to live inventory matrix!", icon="📦")
                    time.sleep(0.4)
                    st.rerun()
                else:
                    st.error("Invalid entry or duplicate product ID name.")
                    
            st.markdown("---")
            st.markdown("##### Add New Supplier Profile")
            new_s_name = st.text_input("Supplier Company Name")
            new_s_email = st.text_input("Authorized Sender Email")
            new_s_phone = st.text_input("Mobile Registry Contact")
            
            if st.button("Save Supplier Node"):
                if new_s_name and validate_email_format(new_s_email):
                    st.session_state.primary_suppliers.append({"name": new_s_name, "email": new_s_email, "phone": new_s_phone})
                    add_log_entry("REGISTRY_EXPANSION", f"Authorized new supplier routing email node: {new_s_email}.")
                    st.toast(f"Supplier {new_s_name} registered successfully!", icon="🚚")
                    time.sleep(0.4)
                    st.rerun()
                else:
                    st.error("Provide a valid company name and correct corporate email schema.")

        # MANUAL INCREMENT & DECREMENT INTERFACE
        st.markdown("---")
        st.markdown("### 📥 Manual Stock Adjustments")
        target_product = st.selectbox("Select Target Product SKU", product_list)
        change_qty = st.number_input("Adjustment Quantity Amount", min_value=1, value=50, step=10)
        
        col_inc, col_dec = st.columns(2)
        with col_inc:
            if st.button("➕ Receive / Add"):
                st.session_state.database[target_product]["stock"] += change_qty
                add_log_entry("MANUAL_INCREMENT", f"Manually added {change_qty} units to {target_product} inventory matrix.")
                st.toast(f"Incremented stock balance!", icon="✅")
                time.sleep(0.4)
                st.rerun()
        with col_dec:
            if st.button("➖ Deduct / Sub"):
                if st.session_state.database[target_product]["stock"] >= change_qty:
                    st.session_state.database[target_product]["stock"] -= change_qty
                    add_log_entry("MANUAL_DECREMENT", f"Manually deducted {change_qty} units from {target_product} inventory balance.")
                    st.toast(f"Deducted stock balance!", icon="📉")
                    time.sleep(0.4)
                    st.rerun()
                else:
                    st.error("Deficit limits prevent subtraction.")

    # App Main Layout Header
    st.title("📦 AutoRoute Dynamic Logi-Agent Panel")
    st.markdown(f"**Operating State:** `State: {st.session_state.system_state}`")
    st.markdown("---")

    tab_live, tab_history = st.tabs(["📊 Screen 1: Live Stock Monitor & Ingestion", "📜 Screen 2: Log Book & Past Sales Data"])

    # ==============================================================================
    # SCREEN 1: LIVE OPERATIONS & INGESTION
    # ==============================================================================
    with tab_live:
        st.subheader("📊 Current Live Inventory Runway Metrics")
        metric_cols = st.columns(len(product_list) + 1)
        
        for idx, prod in enumerate(product_list):
            current_stock = st.session_state.database[prod]["stock"]
            avg_sales = st.session_state.database[prod]["history_avg"]
            
            if not log_sync_success:
                st.session_state.system_state = "ESCALATION_GHOST"
                runway_display = "--"
                delta_msg = "DATA DISCONNECTED"
                delta_col = "inverse"
            else:
                if st.session_state.system_state in ["ESCALATION_GHOST", "UNAUTHORIZED_SENDER_ALERT"] and st.session_state.active_exception is None:
                    st.session_state.system_state = "IDLE"
                runway_days = int(current_stock / avg_sales) if avg_sales > 0 else 0
                runway_display = f"{runway_days} Days"
                delta_msg = "Stable Buffer" if runway_days > 5 else "CRITICAL LOW"
                delta_col = "normal" if runway_days > 5 else "inverse"
                
            with metric_cols[idx]:
                st.metric(label=f"{prod} Balance", value=f"{current_stock} Units", delta=f"{runway_display} Runway", delta_color=delta_col)
                st.progress(min(max(current_stock / 1200.0, 0.0), 1.0))

        with metric_cols[-1]:
            active_exc_label = "1 Exception Open" if st.session_state.active_exception else "0 Exceptions Pending"
            st.metric(label="Network Disrupted Paths", value=active_exc_label, delta="Action Required" if st.session_state.active_exception else "Systems Nominal")

        st.markdown("---")

        # ENGINE STATE RUNNERS
        if st.session_state.system_state == "IDLE":
            st.subheader("📥 Inbound Logistics AI Parsing Gateway")
            col_in_1, col_in_2 = st.columns(2)
            
            with col_in_1:
                st.markdown("##### 🔍 1. Telemetry Sender Verification Gateway")
                sender_email_input = st.text_input("Inbound Message Sender Email Address", value="dispatch@primelogistics.com")
                today_sales_check = st.number_input("Today's Current Inbound Sales Volume", value=int(st.session_state.database[product_list[0]]['history_avg']))
                
            with col_in_2:
                st.markdown("##### 📧 2. Inbound Stream Data Payload")
                email_input_body = st.text_area(
                    "Paste Inbound Operational Message Body Here to Verify Engine Parsing:",
                    value=f"URGENT: Logistics networks report a transit shift. Shipments containing our baseline batch of {product_list[0]} encountered a hold, introducing a 5-day arrival bottleneck."
                )
                
            if st.button("🚀 Execute AI Pipeline Analysis", use_container_width=True):
                # NEW FEATURE: AUTHORIZED SENDER EMAIL GATEKEEPER CHECK
                if sender_email_input not in authorized_emails:
                    st.session_state.system_state = "UNAUTHORIZED_SENDER_ALERT"
                    st.session_state.active_exception = {
                        "sender": sender_email_input,
                        "body": email_input_body
                    }
                    add_log_entry("UNAUTHORIZED_SENDER_INTERCEPT", f"Blocked inbound message execution attempt from external unverified address: {sender_email_input}", "SECURITY_ALERT")
                    st.rerun()

                base_avg = st.session_state.database[product_list[0]]['history_avg']
                # Anomaly Velocity Gate
                if today_sales_check > (base_avg * 3):
                    st.session_state.system_state = "ESCALATION_ANOMALY"
                    st.session_state.active_exception = {"today_sales": today_sales_check}
                    add_log_entry("ANOMALY_BREACH", f"Sales volume spike verified at {today_sales_check} units.", "WARNING")
                    st.rerun()

                # Process verified text payload
                parse_results = run_visual_ai_parsing_pipeline(email_input_body, product_list, st.session_state.primary_suppliers)
                
                st.markdown("#### 🔍 Live Parsing Trace Window")
                st.json(parse_results)
                
                if parse_results['sku']:
                    target_sku = parse_results['sku']
                    avg_consumption = st.session_state.database[target_sku]['history_avg']
                    current_runway = st.session_state.database[target_sku]['stock'] / avg_consumption
                    
                    if current_runway < parse_results['delay_days']:
                        deficit_units = math.ceil((parse_results['delay_days'] - current_runway) * avg_consumption)
                        backup_vendor = st.session_state.backup_ledger[0]
                        
                        st.session_state.active_exception = {
                            "type": "STANDARD_PROCURE" if backup_vendor['price'] == "Valid Margin" and backup_vendor['grade'] == "Premium" else "PREDATORY_SHUTDOWN",
                            "sku": target_sku,
                            "deficit": deficit_units,
                            "delay": parse_results['delay_days'],
                            "node": parse_results['supplier'],
                            "backup": backup_vendor['name']
                        }
                        st.session_state.system_state = "HUMAN_APPROVAL_QUEUE"
                        add_log_entry("EXCEPTION_ROUTING", f"Runway shortfall found for {target_sku}. Deficit requirement calculated at {deficit_units} items.", "CRITICAL")
                        st.rerun()
                    else:
                        st.success(f"🟢 Low Risk Monitor Logged: Sourcing runway covers the parsed delay window safely.")
                        add_log_entry("LOW_RISK_MONITOR", f"Parsed delay window for {target_sku} covered by present stock buffers.")
                else:
                    st.error("❌ Identification Failure: No recognized SKU keyword structure found inside the message string.")

        # NEW STATE FEATURE: UNAUTHORIZED SENDER CRITICAL PROTOCOL SCREEN
        elif st.session_state.system_state == "UNAUTHORIZED_SENDER_ALERT":
            exc = st.session_state.active_exception
            st.error(f"🚨 CRITICAL PROTOCOL ENGAGED: Unverified Data Packet Intercepted from [{exc['sender']}]")
            st.markdown("The system blocked this text payload from auto-parsing because the email is not registered in your authorized sourcing list. Review the details below:")
            
            st.info(f"**Intercepted Message Body Content:**\n\n\"{exc['body']}\"")
            
            c_sec1, c_sec2 = st.columns(2)
            with c_sec1:
                if st.button("🔓 Override & Force Run AI Parser (Trust This Message Once)"):
                    st.session_state.system_state = "IDLE"
                    st.session_state.active_exception = None
                    add_log_entry("SECURITY_OVERRIDE", f"Manager manually bypassed sender filter constraints for packet from {exc['sender']}.")
                    st.toast("Security bypass accepted. Running data extraction pipeline...", icon="🔓")
                    time.sleep(0.5)
                    st.rerun()
            with c_sec2:
                if st.button("🗑️ Reject & Purge Message Packet"):
                    st.session_state.system_state = "IDLE"
                    st.session_state.active_exception = None
                    add_log_entry("SECURITY_PURGE", f"Manager discarded unverified message string from sender entry: {exc['sender']}.")
                    st.toast("Message purged safely from active buffers.", icon="🗑️")
                    time.sleep(0.4)
                    st.rerun()

        # STATE 4: GHOST DATA
        elif st.session_state.system_state == "ESCALATION_GHOST":
            st.error("🚨 Critical Protocol: Ghost Data Protocol Active due to Disconnected Warehouse Sync Logs.")
            st.markdown("### 🧑‍💼 Manager Concurrency Matrix Controls")
            if st.session_state.token_lock_holder is None:
                if st.button("🔑 Request Pipeline Mutation Lock"):
                    st.session_state.token_lock_holder = "Manager A"
                    st.rerun()
            else:
                st.success(f"🔒 Single Lock Lease Exclusively Acquired by: {st.session_state.token_lock_holder}")
                override_units = st.number_input(f"Enter Manually Verified Audit Count for {product_list[0]}:", min_value=0, value=700)
                if st.button("💾 Force Database Sync & Terminate Lock"):
                    st.session_state.database[product_list[0]]['stock'] = override_units
                    st.session_state.token_lock_holder = None
                    st.session_state.system_state = "IDLE"
                    add_log_entry("GHOST_DATA_RESOLVED", f"Manual stock baseline reconciliation set to {override_units} units.")
                    st.rerun()

        # STATE 4: ANOMALY VELOCITY
        elif st.session_state.system_state == "ESCALATION_ANOMALY":
            st.error("🚨 Critical Protocol: Sales Velocity Spike Anomaly Gate Breached (>300% baseline).")
            c_an1, c_an2 = st.columns(2)
            with c_an1:
                if st.button("📊 Classify as Structural New Normal"):
                    st.session_state.database[product_list[0]]['history_avg'] = st.session_state.active_exception['today_sales']
                    add_log_entry("BASELINE_MUTATED", f"Adjusted daily tracking benchmarks permanently to {st.session_state.active_exception['today_sales']}/day.")
                    st.session_state.system_state = "IDLE"
                    st.session_state.active_exception = None
                    st.rerun()
            with c_an2:
                if st.button("⏳ Classify as Isolated One-Time Incident"):
                    st.session_state.system_state = "IDLE"
                    st.session_state.active_exception = None
                    add_log_entry("ANOMALY_IGNORED", "Spike flagged as anomaly outlier. Retained original tracking benchmarks.")
                    st.rerun()

        # STATE 5: HUMAN APPROVAL MITIGATION
        elif st.session_state.system_state == "HUMAN_APPROVAL_QUEUE":
            st.subheader("🔵 State 5: Human Strategy Verification Queue")
            exc = st.session_state.active_exception
            
            if exc['type'] == "STANDARD_PROCURE":
                st.info(f"🛡️ Alternative Sourcing Path Evaluated: Alternative vendor **{exc['backup']}** matches quality and target parameters.")
                if st.button("🔥 One-Click Verification: Dispatch API Signals & Update ERP", use_container_width=True):
                    st.session_state.database[exc['sku']]['stock'] += exc['deficit']
                    add_log_entry("MITIGATION_EXECUTED", f"Rerouted network pipelines to fill shortfall. Added emergency shipment of {exc['deficit']} units to {exc['sku']}.")
                    st.session_state.system_state = "IDLE"
                    st.session_state.active_exception = None
                    st.rerun()
                    
            elif exc['type'] == "PREDATORY_SHUTDOWN":
                st.error("🚨 Sourcing Guardrails Engaged: Sourcing choices locked due to market pricing manipulation / predatory flags.")
                if st.button("🛑 Authorize Emergency Advisory Notice & Return to IDLE", use_container_width=True):
                    add_log_entry("CRITICAL_SHUTDOWN_BROADCAST", f"Emergency broadcast notices dispatched to client nodes regarding {exc['sku']} inventory tracking blocks.", "ALERT")
                    st.session_state.system_state = "IDLE"
                    st.session_state.active_exception = None
                    st.rerun()

# ==============================================================================
# SCREEN 2: LOG BOOK & PAST SALES DATA
# ==============================================================================
    with tab_history:
        # NEW COMPREHENSIVE END OF DAY SNAPSHOT MATRIX TABLE
        st.subheader("📆 Comprehensive End of Day (EOD) Performance Snapshot Ledger")
        st.markdown("This matrix tracks opening stock balances, unit consumption quantities, and closing stock variables captured at every single end-of-day checkpoint run:")
        
        if st.session_state.eod_snapshots:
            eod_df = pd.DataFrame(st.session_state.eod_snapshots)
            st.dataframe(eod_df, use_container_width=True)
        else:
            st.info("No day cycles have been processed yet. Click the '🌙 Close Today & Advance to Tomorrow' button in the sidebar to generate accounting snap ledgers.")
            
        st.markdown("---")
        
        # SYSTEM LOG BOOK
        st.subheader("📜 System Operational Audit Trail (Log Book)")
        st.markdown("All background security blocks, exceptions, registry updates, and manual adjustments are saved below:")
        
        if st.session_state.log_book:
            log_df = pd.DataFrame(st.session_state.log_book)
            st.dataframe(log_df, use_container_width=True)
        else:
            st.info("Log records are currently empty.")
            
        st.markdown("---")
        
        # ACTIVE REGISTRIES VISUAL INSIGHTS
        st.subheader("📋 Active Enterprise Network Registry Profiles")
        c_reg1, c_reg2 = st.columns(2)
        
        with c_reg1:
            st.markdown("##### Authorized Primary Suppliers Contact Framework")
            sup_df = pd.DataFrame(st.session_state.primary_suppliers)
            st.table(sup_df)
            
        with c_reg2:
            st.markdown("##### Dynamic Catalog Inventory Configuration Database")
            catalog_records = []
            for name, info in st.session_state.database.items():
                catalog_records.append({
                    "Product SKU ID": name,
                    "On-Hand Warehouse Inventory": info['stock'],
                    "Baseline Sales (Units / Day)": info['history_avg']
                })
            st.table(pd.DataFrame(catalog_records))
