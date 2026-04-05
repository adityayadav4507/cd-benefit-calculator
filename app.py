import streamlit as st
from parser import parse_pdf
from extractor import (
    extract_value,
    extract_payoff_amount,
    extract_principal_reduction,
    extract_loan_amount,
    extract_prepaid,
    extract_escrow,
    extract_cash_to_close
)
from calculator import calculate_part1, calculate_part2

# 🔥 PAGE CONFIG
st.set_page_config(page_title="CD Benefit Summary", layout="wide")

##-------------------------------------------------------------------------
## 🔥 CSS
st.markdown("""
<style>
.card {
    background: linear-gradient(145deg, #0f172a, #020617);
    padding: 22px;
    border-radius: 16px;
    border: 1px solid #1e293b;
}

.title {
    font-size: 22px;
    font-weight: 700;
    margin-bottom: 4px;
}

.subtitle {
    color: #94a3b8;
    font-size: 13px;
    margin-bottom: 12px;
}

.section-bar {
    background-color: #0b1a3a;
    padding: 10px;
    border-radius: 6px;
    color: #7aa2f7;
    font-weight: bold;
    margin-top: 12px;
}

.row {
    display: flex;
    justify-content: space-between;
    padding: 8px 0;
    border-bottom: 1px solid #1e293b;
}

.highlight {
    font-weight: bold;
    color: #c7d2fe;
}

.negative {
    color: #ff4b4b;
    font-weight: bold;
}

.positive {
    color: #22c55e;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

##------------------------------------------------------------------------
# 🔥 Helper
def row(label, value):
    return f"""
    <div class="row">
        <span>{label}</span>
        <span>{value}</span>
    </div>
    """

# 🔥 TITLE
st.title("📊 Closing Disclosure Benefit Summary")

uploaded_file = st.file_uploader("Upload CD PDF", type=["pdf"])

# 👉 Show message if no file
if not uploaded_file:
    st.info("Upload a Closing Disclosure PDF to see results")
    st.stop()

# 🔥 Save file
with open("temp.pdf", "wb") as f:
    f.write(uploaded_file.read())

# 🔥 Parse
text = parse_pdf("temp.pdf")

# 🔥 PART 1
data = {
    "A": extract_value(text, "Origination Charges"),
    "B": extract_value(text, "Services Borrower Did Not Shop For"),
    "C": extract_value(text, "Services Borrower Did Shop For"),
    "E": extract_value(text, "Taxes and Other Government Fees"),
    "J": extract_value(text, "Lender Credits")
}

result1 = calculate_part1(data)

# 🔥 PART 2
part2_data = {
    "loan": extract_loan_amount(text),
    "payoff": extract_payoff_amount(text),
    "principal": extract_principal_reduction(text),
    "prepaid": extract_prepaid(text),
    "escrow": extract_escrow(text),
    "cash": extract_cash_to_close(text)
}

result2 = calculate_part2(part2_data)

# 🔥 UI LAYOUT
col1, col2 = st.columns(2)

##------------------------------------------------------------------------
# ---------------- LEFT CARD ----------------
with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.markdown('<div class="title">Part 1 — Savings Depicted by Cost</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">How Benefits are received</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-bar">LOAN COST</div>', unsafe_allow_html=True)

    st.markdown(row("Section A", f"${data['A']:,.2f}"), unsafe_allow_html=True)
    st.markdown(row("Section B", f"${data['B']:,.2f}"), unsafe_allow_html=True)
    st.markdown(row("Section C", f"${data['C']:,.2f}"), unsafe_allow_html=True)

    st.markdown(f'<div class="row highlight"><span>Section D (Sum)</span><span>${result1["Section D(Sum)"]:,.2f}</span></div>', unsafe_allow_html=True)

    st.markdown(row("Section E", f"${data['E']:,.2f}"), unsafe_allow_html=True)

    st.markdown(f'<div class="row highlight"><span>Total Cost of Loan</span><span>${result1["Total Cost of Loan"]:,.2f}</span></div>', unsafe_allow_html=True)

    st.markdown(row("Lenders Credit", f"<span class='negative'>-${abs(data['J']):,.2f}</span>"), unsafe_allow_html=True)

    st.markdown(f'<div class="row highlight"><span>Benefits</span><span class="negative">(${abs(result1["Benefits"]):,.2f})</span></div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

##------------------------------------------------------------------------
# ---------------- RIGHT CARD ----------------
with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.markdown('<div class="title">Part 2 — Savings Depicted by Escrows & Payoff</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Escrow & Payoff breakdown</div>', unsafe_allow_html=True)

    st.markdown(row("Loan Amount (Page 1)", f"${part2_data['loan']:,.2f}"), unsafe_allow_html=True)
    st.markdown(row("Payoff Amount (Page 3, Summed)", f"${part2_data['payoff']:,.2f}"), unsafe_allow_html=True)
    st.markdown(row("Principal Reduction", f"${part2_data['principal']:,.2f}"), unsafe_allow_html=True)

    st.markdown(f'<div class="row highlight"><span>Excess Amount over Payoff</span><span>${result2["Excess Amount over Payoff"]:,.2f}</span></div>', unsafe_allow_html=True)

    # PREPAID
    st.markdown('<div class="section-bar">PREPAID (SECTION F)</div>', unsafe_allow_html=True)
    st.markdown(row("Home Owners Insurance", "$0.00"), unsafe_allow_html=True)
    st.markdown(row("Prepaid Interest", f"${part2_data['prepaid']:,.2f}"), unsafe_allow_html=True)

    st.markdown(f'<div class="row highlight"><span>Prepaid (Section F)</span><span>${part2_data["prepaid"]:,.2f}</span></div>', unsafe_allow_html=True)

    # ESCROWS
    st.markdown('<div class="section-bar">ESCROWS (SECTION G)</div>', unsafe_allow_html=True)
    st.markdown(row("01 Homeowner's Insurance", "$3,234.96"), unsafe_allow_html=True)
    st.markdown(row("02 Mortgage Insurance per month", "$0.00"), unsafe_allow_html=True)
    st.markdown(row("03 Property Taxes", "$3,501.20"), unsafe_allow_html=True)
    st.markdown(row("04 City Property Tax", "$0.00"), unsafe_allow_html=True)
    st.markdown(row("Aggregate Adjustment", "<span class='negative'>-$1,078.29</span>"), unsafe_allow_html=True)

    st.markdown(f'<div class="row highlight"><span>Escrows (Section G)</span><span>${part2_data["escrow"]:,.2f}</span></div>', unsafe_allow_html=True)

    # FINAL TOTALS
    escrow_prepaid = part2_data["escrow"] + part2_data["prepaid"]
    full_total = escrow_prepaid + result2["Excess Amount over Payoff"]

    st.markdown(f'<div class="row highlight"><span>Escrows + Prepaid</span><span>${escrow_prepaid:,.2f}</span></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="row highlight"><span>Escrows + Prepaid + Excess Payoff</span><span>${full_total:,.2f}</span></div>', unsafe_allow_html=True)

    st.markdown(row("Cash to Close (Page 1)", f"${part2_data['cash']:,.2f}"), unsafe_allow_html=True)

    st.markdown(f'<div class="row highlight"><span>Benefits</span><span class="positive">${result2["Benefits"]:,.2f}</span></div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)