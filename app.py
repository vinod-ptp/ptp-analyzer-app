import streamlit as st
import pandas as pd

st.title("PTP Transformation Assistant")

# Sidebar
st.sidebar.header("Client Questionnaire")

automation_level = st.sidebar.selectbox(
    "Current Automation Level",
    ["Low", "Medium", "High"]
)

approval_complexity = st.sidebar.selectbox(
    "Approval Complexity",
    ["Simple", "Moderate", "Complex"]
)

invoice_volume = st.sidebar.selectbox(
    "Invoice Volume",
    ["Low (<1000/month)", "Medium (1000-5000)", "High (>5000)"]
)

st.write("Upload your ERP data to begin analysis")

# File Upload
uploaded_file = st.file_uploader("Upload ERP File", type=["csv", "xlsx"])

# 🔒 EVERYTHING BELOW INSIDE THIS BLOCK
if uploaded_file:

    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.subheader("Data Preview")
    st.write(df.head())

    st.subheader("Total Records")
    st.write(len(df))

    # ---------------------------
    # BASIC METRICS
    # ---------------------------
    st.subheader("Basic Metrics")

    total_invoices = len(df)

    if 'Payment_Status' in df.columns:
        on_time = df[df['Payment_Status'] == 'On Time'].shape[0]
        on_time_pct = (on_time / total_invoices) * 100

        st.metric("Total Invoices", total_invoices)
        st.metric("On-Time %", round(on_time_pct, 2))
    else:
        st.warning("Column 'Payment_Status' not found")

    # ---------------------------
    # EXCEPTION ANALYSIS
    # ---------------------------
    st.subheader("Exception Analysis")

    if 'Exception_Type' in df.columns:
        exceptions = df['Exception_Type'].value_counts()
        st.bar_chart(exceptions)
    else:
        st.warning("Column 'Exception_Type' not found")

    # ---------------------------
    # DEPARTMENT ANALYSIS
    # ---------------------------
    st.subheader("Department Analysis")

    if 'Department' in df.columns:
        dept = df['Department'].value_counts()
        st.bar_chart(dept)
    else:
        st.warning("Column 'Department' not found")

    # ---------------------------
    # INSIGHTS
    # ---------------------------
    st.subheader("As-Is Process Insights")

    insights = []

    if 'Payment_Status' in df.columns:
        if on_time_pct < 80:
            insights.append("⚠️ Low on-time payment performance")
        else:
            insights.append("✅ Good on-time performance")

    if 'Exception_Type' in df.columns:
        top_exception = exceptions.idxmax()
        insights.append(f"🔍 Top exception: {top_exception}")

    if 'Department' in df.columns:
        top_dept = dept.idxmax()
        insights.append(f"🏢 Problem department: {top_dept}")

    for i in insights:
        st.write(i)

    # ---------------------------
    # AS-IS PROCESS
    # ---------------------------
    st.subheader("As-Is Process Flow")

    process_steps = [
        "1. Invoice received from vendor",
        "2. Invoice validation and exception check",
        "3. Routed to department for approval",
        "4. Payment processed",
        "5. Manual exception handling",
        "6. Approval delays impact payment"
    ]

    for step in process_steps:
        st.write(step)

    # ---------------------------
    # TO-BE PROCESS
    # ---------------------------
    st.subheader("To-Be Process (Recommended)")

    tobe_steps = [
        "1. Digital invoice intake",
        "2. Automated validation",
        "3. Auto exception handling",
        "4. Workflow-based approval",
        "5. Real-time tracking",
        "6. Automated payment",
        "7. KPI dashboard"
    ]

    for step in tobe_steps:
        st.write(step)
