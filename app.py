import streamlit as st
import pandas as pd

st.title("PTP Transformation Assistant")
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

if uploaded_file:
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.subheader("Data Preview")
    st.write(df.head())

    st.subheader("Total Records")
    st.write(len(df))
    st.subheader("Basic Metrics")

    total_invoices = len(df)

    if 'Payment_Status' in df.columns:
        on_time = df[df['Payment_Status'] == 'On Time'].shape[0]
        on_time_pct = (on_time / total_invoices) * 100

        st.metric("Total Invoices", total_invoices)
        st.metric("On-Time %", round(on_time_pct, 2))
    else:
        st.warning("Column 'Payment_Status' not found in data")
        st.subheader("Exception Analysis")
        st.subheader("Exception Analysis")
if 'Exception_Type' in df.columns:
    exceptions = df['Exception_Type'].value_counts()
    st.bar_chart(exceptions)
else:
    st.warning("Column 'Exception_Type' not found in data")
    st.subheader("Department Analysis")

if 'Department' in df.columns:
    dept = df['Department'].value_counts()
    st.bar_chart(dept)
else:
    st.warning("Column 'Department' not found in data")
    st.subheader("As-Is Process Insights")

insights = []

# On-time performance insight
if 'Payment_Status' in df.columns:
    if on_time_pct < 80:
        insights.append("⚠️ Low on-time payment performance indicating process inefficiencies")
    else:
        insights.append("✅ Good on-time payment performance")

# Exception insight
if 'Exception_Type' in df.columns:
    top_exception = exceptions.idxmax()
    insights.append(f"🔍 Most common exception: {top_exception}")

# Department insight
if 'Department' in df.columns:
    top_dept = dept.idxmax()
    insights.append(f"🏢 Most challenging department: {top_dept}")

# Display insights
for i in insights:
    st.write(i)
    st.subheader("As-Is Process Flow")

process_steps = []

process_steps.append("1. Invoice received from vendor")

if 'Exception_Type' in df.columns:
    process_steps.append("2. Invoice validation and exception check")

if 'Department' in df.columns:
    process_steps.append("3. Invoice routed to respective department for approval")

if 'Payment_Status' in df.columns:
    process_steps.append("4. Payment processing based on approval and due date")

# Add pain points based on insights
process_steps.append("5. Exceptions handled manually causing delays")
process_steps.append("6. Approval delays impacting on-time payment performance")

# Display process
for step in process_steps:
    st.write(step)
    st.subheader("Initial To-Be Process (Recommended)")

tobe_steps = []

tobe_steps.append("1. Invoice received digitally (e-invoice / OCR)")
tobe_steps.append("2. Automated validation and duplicate check")

if 'Exception_Type' in df.columns:
    tobe_steps.append("3. Exceptions auto-classified and routed")

if 'Department' in df.columns:
    tobe_steps.append("4. Automated workflow-based approval")

tobe_steps.append("5. Real-time tracking of invoice status")
tobe_steps.append("6. Automated payment processing")
tobe_steps.append("7. Dashboard for monitoring KPIs")

# Add improvement note
tobe_steps.append("➡️ Reduced manual intervention and improved cycle time")

# Display To-Be process
for step in tobe_steps:
    st.write(step)