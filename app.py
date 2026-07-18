import streamlit as st
import pandas as pd
import math
import time
import re

# 1. Page Configuration
st.set_page_config(page_title="AutoRoute Intelligence Terminal", layout="wide")

# ==============================================================================
# SMART PARSING UTILITIES (The "AI" Intelligence Layer)
# ==============================================================================
def validate_email_format(email_str):
    """Verifies if the string matches a standard corporate email structure."""
    email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return bool(re.match(email_pattern, email_str))

def extract_delay_from_text(text_content):
    """Scans raw text to dynamically extract delay days or hours."""
    # Look for patterns like "4-day" or "3 days"
    day_match = re.search(r"(\d+)\s*-?\s*day", text_content, re.IGNORECASE)
    if day_match:
        return float(day_match.group(1))
        
    # Look for patterns like "48 hours" or "72-hour" and convert to days
    hour_match = re.search(r"(\d+)\s*-?\s*hour", text_content, re.IGNORECASE)
    if hour_match:
        return float(hour_match.group(1)) / 24.0
        
    return 3.0  # Fallback smart estimate if no metric found

def identify_responsible_supplier(text_content, supplier_list):
    """Matches text against registered network entities to find the root node."""
    for supplier in supplier_list:
        if supplier.lower() in text_content.lower():
            return supplier
    return "Unknown Carrier / Supplier"

# ==============================================================================
# STATE INITIALIZATION
# ==============================================================================
if 'onboarded' not in st.session_state:
    st.session_state.onboarded = False
if 'corp_details' not in st.session_state:
    st.session_state.corp_details = {}
if 'suppliers' not in st.session_state:
    st.session_state.suppliers = []
if 'database' not in st.session_state:
    st.session_state.database = {}
if 'system_state' not in st.session_state:
    st.session_state.system_state = "IDLE"
if 'active_exception' not in st.session_state:
    st.session_state.active_exception = None
if 'token_lock_holder' not in st.session_state:
    st.session_state.token_lock_holder = None

# ==============================================================================
# SCREEN A: DYNAMIC CORPORATE ONBOARDING GATEWAY
# ==============================================================================
if not st.session_state.onboarded:
    st.title("🏢 AutoRoute Logi-Agent Enterprise Setup")
    st.markdown("### Initialize Your Custom Supply Chain Terminal")
    st.markdown("---")
    
    with st.form("dynamic_onboarding_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🏢 1. Corporation Contact Profile")
            corp_name = st.text_input("Company / Entity Name", value="Apex Global Tech Distribution")
            reg_number = st.text_input("Business Registration / Tax ID", value="TAX-77-89412")
            email = st.text_input("Corporate Operations Email Address", value="supplychain@apexglobal.com")
            phone = st.text_input("Emergency Mobile Contact", value="+1 (555) 489-1212")
            region = st.selectbox("Active Logistics Zone", ["North America Core", "EMEA Operations", "APAC Network"])
            
            st.markdown("---")
            st.markdown("#### 🚚 2. Supplier Network Registry")
            supplier_raw = st.text_area(
                "Enter Registered Suppliers (Add as many as you want, one per line):",
                value="Prime Logistics Inc.\nNexus Manufacturing Group\nHorizon Freight Global\nPacific Core Logistics\nAtlas Cargo Network"
            )
            
        with col2:
            st.markdown("#### 📦 3. Product Catalog & Current Stock Setup")
            p1_name = st.text_input("Product 1 Name:", value="Wireless Headphones")
            p1_stock = st.number_input("Product 1 Starting Stock:", min_value=0, value=500)
            
            st.markdown("---")
            p2_name = st.text_input("Product 2 Name (Optional):", value="Smart Watches")
            p2_stock = st.number_input("Product 2 Starting Stock:", min_value=0, value=320)
            
        st.markdown("---")
        submit_btn = st.form_submit_button("🚀 Compile Custom Operational Engine")
        
        if submit_btn:
            if not corp_name or not p1_name or not supplier_raw:
                st.error("Setup Failed: Please ensure Company Name, Supplier List, and Product 1 are filled out.")
            elif not validate_email_format(email):
                st.error("❌ Authentication Error: Invalid Corporate Email Address format detected. (e.g., must contain @ and a valid domain extension like .com)")
            else:
                parsed_suppliers = [line.strip() for line in supplier_raw.split("\n") if line.strip()]
                
                dynamic_db = {}
                dynamic_db[p1_name] = {"stock": p1_stock, "daily_sales_history": [25, 24, 26, 25, 23, 27, 25]}
                if p2_name:
                    dynamic_db[p2_name] = {"stock": p2_stock, "daily_sales_history": [15, 14, 16, 15, 14, 17, 15]}
                
                st.session_state.corp_details = {
                    "corp_name": corp_name,
                    "reg_number": reg_number,
                    "email": email,
                    "phone": phone,
                    "region": region
                }
                st.session_state.suppliers = parsed_suppliers
                st.session_state.database = dynamic_db
                st.session_state.onboarded = True
                st.toast("Building your dynamic dashboard environment...", icon="🛠️")
                time.sleep(1)
                st.rerun()

# ==============================================================================
# SCREEN B: DYNAMIC OPERATIONAL PANEL
# ==============================================================================
else:
    product_list = list(st.session_state.database.keys())
    primary_product = product_list[0]
    
    with st.sidebar:
        st.title("🔒 Active Session Context")
        st.info(f"**🏢 Company:** {st.session_state.corp_details['corp_name']}\n\n**🌍 Hub Zone:** {st.session_state.corp_details['region']}")
        
        # Display the completely infinite supplier network cleanly
        st.markdown(f"#### 🚚 Active Suppliers ({len(st.session_state.suppliers)})")
        for sup in st.session_state.suppliers:
            st.markdown(f"- `{sup}`")
            
        if st.button("🚪 Reset Framework & Clear Profile"):
            st.session_state.onboarded = False
            st.session_state.database = {}
            st.session_state.suppliers = []
            st.session_state.system_state = "IDLE"
            st.session_state.active_exception = None
            st.rerun()
            
        st.markdown("---")
        st.title("🗄️ Real-Time Inventory Control")
        log_sync_success = st.checkbox("Synchronize Warehouse Logs Daily", value=True)
        st.markdown("---")
        
        for prod in product_list:
            st.session_state.database[prod]["stock"] = st.number_input(
                f"Adjust {prod} Stock:", min_value=0, value=int(st.session_state.database[prod]["stock"])
            )

    st.title("📦 AutoRoute Dynamic Logi-Agent Panel")
    st.markdown(f"**Operational Corporate Entity:** {st.session_state.corp_details['corp_name']} | Node Contact: *{st.session_state.corp_details['email']}*")
    st.markdown("---")

    st.subheader("📊 Live Inventory Runway Status")
    metric_cols = st.columns(len(product_list) + 1)
    
    for idx, prod in enumerate(product_list):
        avg_sales = sum(st.session_state.database[prod]["daily_sales_history"]) / 7
        current_stock = st.session_state.database[prod]["stock"]
        
        if idx == 0 and not log_sync_success:
            st.session_state.system_state = "ESCALATION_GHOST"
            runway_display = "--"
            delta_msg = "DATA DISCONNECTED"
            delta_col = "inverse"
        else:
            if idx == 0 and st.session_state.system_state == "ESCALATION_GHOST":
                st.session_state.system_state = "IDLE"
            runway_calc = int(current_stock / avg_sales) if avg_sales > 0 else 0
            runway_display = f"{runway_calc} Days"
            delta_msg = "Stable Buffer" if runway_calc > 3 else "CRITICAL LOW"
            delta_col = "normal" if runway_calc > 3 else "inverse"
            
        with metric_cols[idx]:
            st.metric(label=f"{prod} Runway", value=runway_display, delta=delta_msg, delta_color=delta_col)
            st.progress(min(current_stock / 1000.0, 1.0))

    with metric_cols[-1]:
        active_exceptions_num = "1 Active Exception" if st.session_state.active_exception else "0 Active Exceptions"
        st.metric(label="Active Network Disrupted Paths", value=active_exceptions_num, 
                  delta="Action Required" if st.session_state.active_exception else "All Systems Nominal")

    st.markdown("---")

    if st.session_state.system_state == "IDLE":
        st.subheader("📥 Inbound Logistics AI Parsing Gateway")
        
        # We drop one of our dynamic supplier names directly into the starting text to prove it works!
        demo_supplier = st.session_state.suppliers[1] if len(st.session_state.suppliers) > 1 else "Nexus Manufacturing Group"
        
        email_input = st.text_area(
            "Paste Raw Inbound Exception Notification (Try changing the '5-day' text or the supplier name to test the extraction engine!):",
            value=f"URGENT: Management teams at {demo_supplier} have flagged a distribution delay. The container stack holding our core shipment of {primary_product} has encountered a customs hold, forcing a structural 5-day arrival delay to hubs."
        )
        
        if st.button("🚀 Execute AI Pipeline Analysis"):
            if primary_product.lower() in email_input.lower():
                avg_sales = sum(st.session_state.database[primary_product]["daily_sales_history"]) / 7
                current_runway = st.session_state.database[primary_product]["stock"] / avg_sales
                
                # Dynamic intelligence extractions
                parsed_delay = extract_delay_from_text(email_input)
                faulty_supplier = identify_responsible_supplier(email_input, st.session_state.suppliers)
                
                if current_runway < parsed_delay:
                    st.session_state.active_exception = {
                        "sku": primary_product,
                        "delay_days": parsed_delay,
                        "deficit_days": parsed_delay - current_runway,
                        "avg_sales": avg_sales,
                        "supplier": faulty_supplier
                    }
                    st.session_state.system_state = "APPROVAL_QUEUE"
                    st.rerun()
                else:
                    st.success(f"Analysis complete: Current inventory runway for {primary_product} safely absorbs the dynamic {parsed_delay:.1f}-day delay.")
            else:
                st.warning(f"AI Scanner completed: No operational matches targeting item catalog tracking parameters ({primary_product}) detected.")

    elif st.session_state.system_state == "APPROVAL_QUEUE" and st.session_state.active_exception:
        st.subheader("🔵 Action Center: Pending Disruption Mitigation")
        exc = st.session_state.active_exception
        
        left_panel, right_panel = st.columns(2)
        with left_panel:
            st.markdown("#### 📧 Automated Supplier SLA Claim Notification")
            # The form text updates completely dynamically based on the parsed supplier data
            st.text_area(
                label="Generated Output Content", 
                value=f"ATTN: Contract Compliance Team at {exc['supplier']},\n\nOur system tracking records a structural {exc['delay_days']:.1f}-day transit exception caused by your shipping node. This directly breaks our delivery window parameters for entity {st.session_state.corp_details['corp_name']}.", 
                height=140
            )
            if st.button("✉ " + "Dispatch Verified SLA Claim"):
                st.toast(f"Claim successfully routed directly to database node for: {exc['supplier']}")
                
        with right_panel:
            st.markdown("#### 🛒 Spot Market Procurement Requisition")
            calculated_deficit_units = math.ceil(exc['deficit_days'] * exc['avg_sales'])
            calculated_total_cost = calculated_deficit_units * 12.50
            
            st.metric(f"Calculated Deficit Units of {exc['sku']}", value=calculated_deficit_units)
            st.metric("Total Order Cost Capped", value=f"${calculated_total_cost:,.2f}")
            
            if st.button("💳 Authorize Purchase Order"):
                st.session_state.database[exc['sku']]["stock"] += calculated_deficit_units
                st.session_state.system_state = "IDLE"
                st.session_state.active_exception = None
                st.rerun()

    elif st.session_state.system_state == "ESCALATION_GHOST":
        st.subheader("🚨 Escalation Center: Data Sync Breakout")
        st.code(f"[ALERT] - Circuit Breaker Tripped: Data sync interrupted.\nEmergency Contact Node: {st.session_state.corp_details['phone']}", language="text")
        
        if st.session_state.token_lock_holder is None:
            if st.button("🔑 Acquire Data Input Lock"):
                st.session_state.token_lock_holder = st.session_state.corp_details['corp_name']
                st.rerun()
        else:
            st.info(f"👤 Lock active for token lease holder: {st.session_state.token_lock_holder}")
            manual_override_val = st.number_input(f"Enter Physical Count for {primary_product}:", min_value=0, value=600)
            
            if st.button("💾 Force Database Override Sync"):
                st.session_state.database[primary_product]["stock"] = manual_override_val
                st.session_state.token_lock_holder = None
                st.rerun()
