import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="PayPulse AI",
    page_icon="💳",
    layout="wide"
)

st.title("💳 PayPulse AI")
st.write("AI Revenue Recovery Assistant")

st.divider()

# =========================
# UPLOAD PAYMENT DATA
# =========================

st.header("📂 Upload Payment Data")

uploaded_file = st.file_uploader(
    "Upload your payments.csv file",
    type=["csv"]
)

if uploaded_file is not None:

    data = pd.read_csv(uploaded_file)

    st.success("Payment file uploaded successfully! ✅")

    # =========================
    # CHECK CSV
    # =========================

    required_columns = [
        "Transaction",
        "Customer",
        "Amount",
        "Problem"
    ]

    missing = [
        column
        for column in required_columns
        if column not in data.columns
    ]

    if missing:

        st.error(
            "Missing columns: " + ", ".join(missing)
        )

        st.stop()

    # =========================
    # RECOVERY SCORE
    # =========================

    def get_score(problem):

        if problem == "Bank Declined":
            return 80

        elif problem == "Network Error":
            return 70

        elif problem == "Insufficient Funds":
            return 50

        elif problem == "Expired Card":
            return 30

        return 20

    data["Recovery Score"] = data[
        "Problem"
    ].apply(get_score)

    # =========================
    # RECOVERY ACTION
    # =========================

    def get_action(problem):

        if problem == "Bank Declined":
            return "Retry payment after a short delay"

        elif problem == "Network Error":
            return "Ask customer to retry payment"

        elif problem == "Insufficient Funds":
            return "Send payment reminder"

        elif problem == "Expired Card":
            return "Ask customer to update card"

        return "Contact customer"

    data["Recovery Action"] = data[
        "Problem"
    ].apply(get_action)

    # =========================
    # POTENTIAL RECOVERY
    # =========================

    data["Potential Recovery"] = (
        data["Amount"]
        * data["Recovery Score"]
        / 100
    )

    # =========================
    # PRIORITY
    # =========================

    def get_priority(row):

        score = row["Recovery Score"]
        amount = row["Amount"]

        if score >= 70 and amount >= 5000:
            return "HIGH"

        elif score >= 50:
            return "MEDIUM"

        else:
            return "LOW"

    data["Priority"] = data.apply(
        get_priority,
        axis=1
    )

    # =========================
    # DASHBOARD
    # =========================

    st.header("📊 Revenue Recovery Dashboard")

    total_failed = len(data)

    revenue_at_risk = data[
        "Amount"
    ].sum()

    potential_recovery = data[
        "Potential Recovery"
    ].sum()

    high_priority = len(
        data[
            data["Priority"] == "HIGH"
        ]
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "💳 Failed Payments",
            total_failed
        )

    with col2:

        st.metric(
            "💰 Revenue at Risk",
            f"₹{revenue_at_risk:,.0f}"
        )

    with col3:

        st.metric(
            "💵 Potential Recovery",
            f"₹{potential_recovery:,.0f}"
        )

    with col4:

        st.metric(
            "🔴 High Priority",
            high_priority
        )

    st.divider()

    # =========================
    # PAYMENT TABLE
    # =========================

    st.subheader("💰 Payment Analysis")

    st.dataframe(
        data[
            [
                "Transaction",
                "Customer",
                "Amount",
                "Problem",
                "Recovery Score",
                "Potential Recovery",
                "Priority",
                "Recovery Action"
            ]
        ],
        use_container_width=True
    )

    st.divider()

    # =========================
    # RECOVERY PRIORITY QUEUE
    # =========================

    st.header("🎯 Recovery Priority Queue")

    priority_number = {
        "HIGH": 1,
        "MEDIUM": 2,
        "LOW": 3
    }

    data["Priority Number"] = data[
        "Priority"
    ].map(priority_number)

    queue = data.sort_values(
        by=[
            "Priority Number",
            "Potential Recovery"
        ],
        ascending=[
            True,
            False
        ]
    )

    st.dataframe(
        queue[
            [
                "Transaction",
                "Customer",
                "Amount",
                "Problem",
                "Recovery Score",
                "Potential Recovery",
                "Priority",
                "Recovery Action"
            ]
        ],
        use_container_width=True
    )

    st.divider()

    # =========================
    # RECOVERY ASSISTANT
    # =========================

    st.header("🤖 AI Recovery Assistant")

    transaction = st.selectbox(
        "Select a failed payment",
        data["Transaction"].tolist()
    )

    payment = data[
        data["Transaction"] == transaction
    ].iloc[0]

    customer = payment["Customer"]
    amount = payment["Amount"]
    problem = payment["Problem"]
    score = payment["Recovery Score"]
    priority = payment["Priority"]
    potential = payment["Potential Recovery"]
    action = payment["Recovery Action"]

    st.subheader("🔍 Payment Analysis")

    col1, col2 = st.columns(2)

    with col1:

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

        st.write(
            f"**Priority:** {priority}"
        )

    with col2:

        st.metric(
            "Recovery Score",
            f"{score}/100"
        )

        st.metric(
            "Potential Recovery",
            f"₹{potential:,.0f}"
        )

    st.divider()

    # =========================
    # RECOVERY STRATEGY ENGINE
    # =========================

    st.header(
        "🧠 Revenue Recovery Strategy Engine"
    )

    st.write(
        "PayPulse analyzes the failure reason, "
        "payment amount and recovery score to "
        "select the most suitable recovery strategy."
    )

    # Strategy selection

    if problem == "Bank Declined":

        strategy = "Smart Retry"

        explanation = (
            "The payment has a relatively high recovery "
            "opportunity. A retry after a short delay "
            "may successfully recover the payment."
        )

        retry = "Retry after a short delay"

        alternative = (
            "Offer another payment method if retry fails."
        )

        customer_message = (
            f"Hi {customer}, your payment of "
            f"₹{amount:,.0f} was declined by your bank. "
            "Please try the payment again after a short while. "
            "You can also use another payment method."
        )

    elif problem == "Network Error":

        strategy = "Retry Immediately"

        explanation = (
            "The failure may be temporary. "
            "A retry is appropriate because network "
            "errors can be transient."
        )

        retry = "Retry the payment"

        alternative = (
            "Ask the customer to use another network "
            "or payment method."
        )

        customer_message = (
            f"Hi {customer}, your payment of "
            f"₹{amount:,.0f} could not be completed "
            "because of a temporary connection issue. "
            "Please try again."
        )

    elif problem == "Insufficient Funds":

        strategy = "Payment Reminder"

        explanation = (
            "Immediately retrying may have a low chance "
            "of success. A reminder gives the customer "
            "time to make funds available."
        )

        retry = "Retry after customer confirms funds"

        alternative = (
            "Offer another available payment method."
        )

        customer_message = (
            f"Hi {customer}, your payment of "
            f"₹{amount:,.0f} could not be completed. "
            "Please check your account balance and try again "
            "when sufficient funds are available."
        )

    elif problem == "Expired Card":

        strategy = "Payment Method Update"

        explanation = (
            "The current card may no longer be valid. "
            "Updating the payment method is more useful "
            "than repeatedly retrying the transaction."
        )

        retry = "Do not repeatedly retry the old card"

        alternative = (
            "Ask the customer to update the card "
            "or use another payment method."
        )

        customer_message = (
            f"Hi {customer}, your payment of "
            f"₹{amount:,.0f} could not be completed "
            "because your card may have expired. "
            "Please update your card or use another payment method."
        )

    else:

        strategy = "Manual Review"

        explanation = (
            "The failure reason is not recognized. "
            "Manual review is recommended before retrying."
        )

        retry = "Review before retrying"

        alternative = (
            "Contact the customer for another payment method."
        )

        customer_message = (
            f"Hi {customer}, we could not complete "
            f"your payment of ₹{amount:,.0f}. "
            "Please try another payment method."
        )

    # =========================
    # DISPLAY STRATEGY
    # =========================

    st.success(
        f"Recommended Strategy: {strategy}"
    )

    st.write(
        f"**Why:** {explanation}"
    )

    st.write(
        f"**Retry Decision:** {retry}"
    )

    st.write(
        f"**Alternative:** {alternative}"
    )

    st.metric(
        "Estimated Recovery Opportunity",
        f"₹{potential:,.0f}"
    )

    st.divider()

    # =========================
    # CUSTOMER MESSAGE
    # =========================

    st.subheader(
        "📩 Personalized Customer Message"
    )

    st.text_area(
        "Recovery message",
        customer_message,
        height=150
    )

    st.divider()

    # =========================
    # AGENT DECISION
    # =========================

    st.header("⚡ Recovery Agent Decision")

    st.write(
        "PayPulse converts the payment analysis into "
        "a recommended next action."
    )

    if priority == "HIGH":

        st.success(
            "🔴 HIGH PRIORITY\n\n"
            "1. Send customer recovery message\n"
            "2. Retry payment after the recommended delay\n"
            "3. Offer an alternative payment method\n"
            "4. Monitor the transaction"
        )

    elif priority == "MEDIUM":

        st.warning(
            "🟡 MEDIUM PRIORITY\n\n"
            "1. Send payment reminder\n"
            "2. Allow customer to retry\n"
            "3. Monitor payment status"
        )

    else:

        st.info(
            "🟢 LOW PRIORITY\n\n"
            "1. Contact customer\n"
            "2. Request payment method update\n"
            "3. Retry later"
        )

    st.divider()

    # =========================
    # STATISTICS
    # =========================

    st.subheader(
        "📊 Failure Statistics"
    )

    st.bar_chart(
        data["Problem"].value_counts()
    )

    st.success(
        "PayPulse AI revenue recovery analysis completed! 🚀"
    )
    # =========================
# RECOVERY SIMULATION
# =========================

st.header("🚀 Recovery Simulation")

st.write(
    "Simulate what happens when PayPulse executes "
    "the recommended recovery strategy."
)

if st.button("▶️ Simulate Recovery"):

    if priority == "HIGH":

        st.success(
            f"Recovery action started for {transaction}."
        )

        st.write(
            "Step 1 ✅ Customer recovery message prepared"
        )

        st.write(
            "Step 2 ✅ Payment retry scheduled"
        )

        st.write(
            "Step 3 ✅ Alternative payment method offered"
        )

        st.write(
            "Step 4 ✅ Transaction added to monitoring"
        )

        st.success(
            f"Potential revenue targeted: ₹{potential:,.0f}"
        )

    elif priority == "MEDIUM":

        st.warning(
            f"Recovery reminder started for {transaction}."
        )

        st.write(
            "Step 1 ✅ Payment reminder prepared"
        )

        st.write(
            "Step 2 ✅ Customer retry requested"
        )

        st.write(
            "Step 3 ✅ Payment monitoring enabled"
        )

        st.info(
            f"Potential revenue targeted: ₹{potential:,.0f}"
        )

    else:

        st.info(
            f"Low-priority recovery workflow started "
            f"for {transaction}."
        )

        st.write(
            "Step 1 ✅ Customer contact recommended"
        )

        st.write(
            "Step 2 ✅ Payment method update requested"
        )

        st.write(
            "Step 3 ✅ Retry scheduled for later"
        )

        st.info(
            f"Potential revenue targeted: ₹{potential:,.0f}"
        )
        # =========================
# RECOVERY SUMMARY
# =========================

st.divider()

st.header("📋 Recovery Summary")

total_recovery_opportunity = data[
    "Potential Recovery"
].sum()

high_value_payments = data[
    data["Priority"] == "HIGH"
]

st.write(
    f"PayPulse identified **{len(high_value_payments)} high-priority "
    f"payment(s)** requiring immediate attention."
)

st.write(
    f"Total revenue at risk: "
    f"**₹{data['Amount'].sum():,.0f}**"
)

st.write(
    f"Estimated recovery opportunity: "
    f"**₹{total_recovery_opportunity:,.0f}**"
)

st.write(
    "The recovery engine prioritizes failed payments "
    "based on failure reason, transaction value, and "
    "estimated recovery probability."
)

st.success(
    "✅ Recovery analysis ready for action"
)