import streamlit as st
import pandas as pd

# ------------------------------------------------------------
# Page Configuration
# ------------------------------------------------------------

st.set_page_config(
    page_title="Azure Cost Chargeback",
    page_icon="☁️",
    layout="wide"
)

# ------------------------------------------------------------
# Load Data
# ------------------------------------------------------------

report = pd.read_csv("output/chargeback_report.csv")
audit = pd.read_csv("output/allocation_audit.csv")

# ------------------------------------------------------------
# Title
# ------------------------------------------------------------

st.title("☁️ Azure Cost Allocation & Chargeback Dashboard")
st.caption("Demonstration Cost Dataset")

# ------------------------------------------------------------
# Calculate Metrics
# ------------------------------------------------------------

total_cost = report["chargeback_total"].sum()
direct_cost = report["direct_cost"].sum()
shared_cost = report["shared_allocated"].sum()
variance = total_cost - (direct_cost + shared_cost)

# ------------------------------------------------------------
# KPI Cards
# ------------------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Cost", f"₹{total_cost:,.0f}")
col2.metric("Direct Cost", f"₹{direct_cost:,.0f}")
col3.metric("Shared Cost", f"₹{shared_cost:,.0f}")
col4.metric("Variance", f"₹{variance:,.0f}")

st.divider()

# ------------------------------------------------------------
# Department Chargeback
# ------------------------------------------------------------

st.subheader("Department Chargeback")

st.dataframe(
    report[
        [
            "department",
            "direct_cost",
            "shared_allocated",
            "chargeback_total"
        ]
    ],
    use_container_width=True,
    hide_index=True
)

# ------------------------------------------------------------
# Charts
# ------------------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    st.subheader("Chargeback by Department")

    chart_data = report.set_index("department")[
        "chargeback_total"
    ]

    st.bar_chart(chart_data)

with col2:

    st.subheader("Shared Cost Allocation")

    allocation_data = report.set_index("department")[
        "shared_allocated"
    ]

    st.bar_chart(allocation_data)

# ------------------------------------------------------------
# Audit Trail
# ------------------------------------------------------------

st.subheader("Shared Cost Allocation Audit Trail")

st.dataframe(
    audit,
    use_container_width=True,
    hide_index=True
)

# ------------------------------------------------------------
# Reconciliation
# ------------------------------------------------------------

st.subheader("Reconciliation")

if abs(variance) < 0.01:
    st.success(
        "PASS — Chargeback reconciles with the demonstration cost dataset."
    )
else:
    st.error(
        f"FAIL — Variance detected: ₹{variance:,.2f}"
    )

# ------------------------------------------------------------
# Footer
# ------------------------------------------------------------

st.caption(
    "Azure Cost Allocation & Chargeback Model | "
    "Demonstration / Synthetic Cost Dataset"
)
