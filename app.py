import streamlit as st
import pandas as pd
import textwrap


st.set_page_config(
    page_title="PayPulse AI",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown(
    """
<style>

.stApp {
    background-color: #f7f9fc;
}

.main .block-container {
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

section[data-testid="stSidebar"] {
    background-color: white;
    border-right: 1px solid #e5e7eb;
}

h1, h2, h3 {
    color: #111827 !important;
}

p {
    color: #4b5563;
}

[data-testid="stMetric"] {
    background-color: white;
    border: 1px solid #e5e7eb;
    border-radius: 16px;
    padding: 18px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.05);
}

[data-testid="stMetricLabel"] {
    color: #6b7280 !important;
    font-weight: 600 !important;
}

[data-testid="stMetricValue"] {
    color: #111827 !important;
    font-weight: 800 !important;
}

.stButton > button {
    border-radius: 10px;
    font-weight: 700;
    padding: 10px 20px;
}

[data-testid="stFileUploader"] {
    background-color: white;
    border: 2px dashed #bfdbfe;
    border-radius: 16px;
    padding: 15px;
}

</style>
""",
    unsafe_allow_html=True
)


with st.sidebar:

    st.markdown(
        """
        <div style="text-align:center; padding:10px 0 20px 0;">
            <div style="font-size:42px;">💳</div>
            <h2 style="margin:0;">PayPulse AI</h2>
            <p style="margin-top:5px;">
                Revenue Recovery
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown("### 🧭 Navigation")

    st.info(
        "Upload payment data below to start the recovery analysis."
    )

    st.divider()

    st.markdown("### 💰 About PayPulse")

    st.caption(
        "PayPulse analyzes failed payments, "
        "estimates recovery opportunities, "
        "and recommends recovery actions."
    )

    st.divider()

    st.caption("PayPulse AI")
    st.caption("Revenue Recovery Assistant")


header_html = """
<div style="
background: linear-gradient(135deg, #1d4ed8, #2563eb);
padding: 32px;
border-radius: 20px;
margin-bottom: 25px;
box-shadow: 0 10px 30px rgba(37, 99, 235, 0.20);
">

<div style="
color: white;
font-size: 42px;
font-weight: 800;
">
💳 PayPulse AI
</div>

<div style="
color: #dbeafe;
font-size: 18px;
margin-top: 8px;
">
Revenue Recovery Assistant for Failed Payments
</div>

</div>
"""

st.markdown(
    textwrap.dedent(header_html),
    unsafe_allow_html=True
)


st.divider()

st.header("📂 Upload Payment Data")

st.write("Upload your payment CSV file.")

uploaded_file = st.file_uploader(
    "Upload payments.csv",
    type=["csv"]
)


if uploaded_file is None:

    st.info(
        "👆 Upload your payments.csv file to start the analysis."
    )

    st.subheader("Required CSV format")

    example_data = pd.DataFrame(
        {
            "Transaction": ["TXN001", "TXN002", "TXN003"],
            "Customer": ["Rahul", "Priya", "Amit"],
            "Amount": [8500, 2000, 5500],
            "Problem": [
                "Bank Declined",
                "Expired Card",
                "Insufficient Funds"
            ]
        }
    )

    st.dataframe(
        example_data,
        use_container_width=True,
        hide_index=True
    )

    st.stop()


try:

    data = pd.read_csv(uploaded_file)

except Exception:

    st.error("❌ Could not read the CSV file.")

    st.write(
        "Please make sure you are uploading a valid CSV file."
    )

    st.stop()


data.columns = (
    data.columns
    .astype(str)
    .str.strip()
)



required_columns = [
    "Transaction",
    "Customer",
    "Amount",
    "Problem"
]

missing_columns = [
    column
    for column in required_columns
    if column not in data.columns
]

if missing_columns:

    st.error(
        "❌ Missing columns: "
        + ", ".join(missing_columns)
    )

    st.write("Your CSV must contain:")

    st.code(
        "Transaction,Customer,Amount,Problem"
    )

    st.stop()



data["Amount"] = pd.to_numeric(
    data["Amount"],
    errors="coerce"
)

data = data.dropna(
    subset=["Amount"]
).copy()

data["Transaction"] = (
    data["Transaction"]
    .astype(str)
    .str.strip()
)

data["Customer"] = (
    data["Customer"]
    .astype(str)
    .str.strip()
)

data["Problem"] = (
    data["Problem"]
    .astype(str)
    .str.strip()
)

if data.empty:

    st.error(
        "❌ No valid payment records were found."
    )

    st.stop()

st.success(
    f"✅ Payment file uploaded successfully! "
    f"{len(data)} payment(s) found."
)


def calculate_recovery_score(row):

    problem = str(row["Problem"]).lower()
    amount = float(row["Amount"])

    if "network" in problem:
        score = 80

    elif "declined" in problem:
        score = 70

    elif "expired" in problem:
        score = 60

    elif "insufficient" in problem:
        score = 50

    else:
        score = 40

    if amount >= 10000:
        score += 10

    elif amount >= 5000:
        score += 5

    return max(0, min(score, 100))



def calculate_priority(score):

    if score >= 75:
        return "HIGH"

    elif score >= 50:
        return "MEDIUM"

    else:
        return "LOW"


def get_strategy(problem, priority):

    problem = str(problem).lower()

    if "network" in problem:
        return "Retry Payment"

    elif "expired" in problem:
        return "Ask Customer to Update Card"

    elif "insufficient" in problem:
        return "Send Payment Reminder"

    elif "declined" in problem:
        return "Offer Alternative Payment Method"

    elif priority == "HIGH":
        return "Immediate Customer Follow-up"

    elif priority == "MEDIUM":
        return "Send Payment Reminder"

    else:
        return "Monitor and Follow Up Later"


def create_customer_message(customer, amount, problem):

    problem_lower = str(problem).lower()

    if "insufficient" in problem_lower:

        return (
            f"Hi {customer}, your payment of "
            f"₹{amount:,.0f} could not be completed "
            f"because sufficient funds were not available. "
            f"Please check your account balance and try again."
        )

    elif "expired" in problem_lower:

        return (
            f"Hi {customer}, your payment of "
            f"₹{amount:,.0f} could not be completed "
            f"because your payment card may have expired. "
            f"Please update your payment method and try again."
        )

    elif "network" in problem_lower:

        return (
            f"Hi {customer}, your payment of "
            f"₹{amount:,.0f} could not be completed "
            f"because of a temporary network issue. "
            f"Please try again."
        )

    elif "declined" in problem_lower:

        return (
            f"Hi {customer}, your payment of "
            f"₹{amount:,.0f} was declined. "
            f"Please try another payment method."
        )

    else:

        return (
            f"Hi {customer}, your payment of "
            f"₹{amount:,.0f} could not be completed. "
            f"Please try again or use another payment method."
        )


data["Recovery Score"] = data.apply(
    calculate_recovery_score,
    axis=1
)

data["Priority"] = data["Recovery Score"].apply(
    calculate_priority
)

data["Potential Recovery"] = (
    data["Amount"]
    * data["Recovery Score"]
    / 100
)

data["Recommended Strategy"] = data.apply(
    lambda row: get_strategy(
        row["Problem"],
        row["Priority"]
    ),
    axis=1
)

st.divider()

st.header("📊 Revenue Recovery Dashboard")

total_payments = len(data)

total_revenue = float(
    data["Amount"].sum()
)

total_recovery = float(
    data["Potential Recovery"].sum()
)

high_priority_count = len(
    data[data["Priority"] == "HIGH"]
)

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Failed Payments",
        total_payments
    )

with col2:

    st.metric(
        "Revenue at Risk",
        f"₹{total_revenue:,.0f}"
    )

with col3:

    st.metric(
        "Potential Recovery",
        f"₹{total_recovery:,.0f}"
    )

with col4:

    st.metric(
        "High Priority",
        high_priority_count
    )


st.subheader("📋 Payment Analysis")

display_columns = [
    "Transaction",
    "Customer",
    "Amount",
    "Problem",
    "Recovery Score",
    "Priority",
    "Potential Recovery",
    "Recommended Strategy"
]

st.dataframe(
    data[display_columns],
    use_container_width=True,
    hide_index=True
)

st.divider()

st.header("🤖 AI Recovery Assistant")

transaction_options = (
    data["Transaction"]
    .astype(str)
    .tolist()
)

selected_transaction = st.selectbox(
    "Select a failed payment",
    transaction_options
)

selected_rows = data[
    data["Transaction"].astype(str)
    == selected_transaction
]

if selected_rows.empty:

    st.error("Payment could not be found.")

    st.stop()

selected_row = selected_rows.iloc[0]

transaction = selected_row["Transaction"]

customer = selected_row["Customer"]

amount = float(
    selected_row["Amount"]
)

problem = selected_row["Problem"]

score = int(
    selected_row["Recovery Score"]
)

priority = selected_row["Priority"]

potential = float(
    selected_row["Potential Recovery"]
)

strategy = selected_row[
    "Recommended Strategy"
]

st.subheader("🔍 Payment Analysis")

left, right = st.columns(2)

with left:

    st.write(
        f"**Transaction:** {transaction}"
    )

    st.write(
        f"**Customer:** {customer}"
    )

    st.write(
        f"**Amount:** ₹{amount:,.0f}"
    )

    st.write(
        f"**Failure Reason:** {problem}"
    )

with right:

    st.write(
        f"**Priority:** {priority}"
    )

    st.metric(
        "Recovery Score",
        f"{score}/100"
    )

    st.metric(
        "Potential Recovery",
        f"₹{potential:,.0f}"
    )


st.divider()

st.subheader("📩 Customer Recovery Message")

message = create_customer_message(
    customer,
    amount,
    problem
)

st.success(message)

st.text_area(
    "Message to send",
    value=message,
    height=120
)


st.divider()

st.subheader("🧠 Recovery Strategy")

st.info(
    f"**Recommended Strategy:** {strategy}"
)


st.header("🤖 Auto Recovery Plan")

st.write(
    "PayPulse creates a recovery workflow "
    "based on the failure reason and priority."
)

if priority == "HIGH":

    st.warning(
        "🔴 HIGH PRIORITY → Immediate customer "
        "follow-up → Offer alternative payment "
        "method → Monitor payment."
    )

elif priority == "MEDIUM":

    st.info(
        "🟡 MEDIUM PRIORITY → Send payment reminder "
        "→ Allow customer to retry → Monitor payment."
    )

else:

    st.success(
        "🟢 LOW PRIORITY → Notify customer "
        "→ Allow retry later → Monitor payment."
    )


st.divider()

st.header("🚀 Recovery Simulation")

st.write(
    "Simulate what happens when PayPulse "
    "executes the recommended recovery strategy."
)

if st.button("▶️ Simulate Recovery"):

    st.success(
        f"Recovery workflow started for {transaction}."
    )

    st.write(
        "Step 1 ✅ Recovery message prepared"
    )

    if priority == "HIGH":

        st.write(
            "Step 2 ✅ Immediate customer follow-up"
        )

        st.write(
            "Step 3 ✅ Alternative payment method offered"
        )

    elif priority == "MEDIUM":

        st.write(
            "Step 2 ✅ Payment reminder prepared"
        )

        st.write(
            "Step 3 ✅ Customer retry requested"
        )

    else:

        st.write(
            "Step 2 ✅ Customer contact recommended"
        )

        st.write(
            "Step 3 ✅ Retry scheduled for later"
        )

    st.write(
        "Step 4 ✅ Payment monitoring enabled"
    )

    st.info(
        f"Potential recovery opportunity: "
        f"₹{potential:,.0f}"
    )

    st.caption(
        "This is a simulation. "
        "No real payment is processed."
    )



st.divider()

st.header("📋 Recovery Summary")

high_count = len(
    data[data["Priority"] == "HIGH"]
)

medium_count = len(
    data[data["Priority"] == "MEDIUM"]
)

low_count = len(
    data[data["Priority"] == "LOW"]
)

st.write(
    f"PayPulse identified **{high_count} high-priority "
    f"payment(s)** requiring immediate attention."
)

st.write(
    f"Total revenue at risk: "
    f"**₹{total_revenue:,.0f}**"
)

st.write(
    f"Estimated recovery opportunity: "
    f"**₹{total_recovery:,.0f}**"
)

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "🔴 High Priority",
        high_count
    )

with col2:

    st.metric(
        "🟡 Medium Priority",
        medium_count
    )

with col3:

    st.metric(
        "🟢 Low Priority",
        low_count
    )



st.divider()

st.header("📊 Failure Statistics")

failure_counts = (
    data["Problem"]
    .value_counts()
    .rename_axis("Failure Reason")
    .reset_index(name="Number of Payments")
)

st.dataframe(
    failure_counts,
    use_container_width=True,
    hide_index=True
)

if not failure_counts.empty:

    st.bar_chart(
        failure_counts.set_index(
            "Failure Reason"
        )
    )


st.divider()

st.header("📥 Download Recovery Report")

report = data.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    "⬇️ Download Recovery Report",
    data=report,
    file_name="paypulse_recovery_report.csv",
    mime="text/csv"
)


st.divider()

st.markdown(
    """
    <div style="
        text-align:center;
        padding:20px;
        color:#6b7280;
    ">
        <b>💳 PayPulse AI</b><br>
        Revenue Recovery Assistant<br><br>
        <small>
        Demonstration project using simulated payment data.<br>
        No real payments are processed.
        </small>
    </div>
    """,
    unsafe_allow_html=True
)
