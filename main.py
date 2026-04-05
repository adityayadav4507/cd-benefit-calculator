from parser import parse_pdf
from extractor import extract_value
from calculator import calculate_part1,calculate_part2

text = parse_pdf("data/sample-cd.pdf")

def extract_all_values(text):
    return {
        "A": extract_value(text, "Origination Charges"),
        "B": extract_value(text, "Services Borrower Did Not Shop For"),
        "C": extract_value(text, "Services Borrower Did Shop For"),
        "E": extract_value(text, "Taxes and Other Government Fees"),
        "J": extract_value(text, "Lender Credits")
    }
data = extract_all_values(text)
result = calculate_part1(data)
print(result)

##--------------------------------------------------------
## Part 2:

from extractor import (
    extract_payoff_amount,
    extract_principal_reduction,
    extract_loan_amount,
    extract_prepaid,
    extract_escrow,
    extract_cash_to_close
)

part2_data = {
    "loan": extract_loan_amount(text),
    "payoff": extract_payoff_amount(text),
    "principal": extract_principal_reduction(text),
    "prepaid": extract_prepaid(text),
    "escrow": extract_escrow(text),
    "cash": extract_cash_to_close(text)
}

result2 = calculate_part2(part2_data)
print(result2)

import os
import json

# create folder if not exists
os.makedirs("outputs", exist_ok=True)

# TEXT OUTPUT
with open("outputs/output.txt", "w") as f:
    f.write("===== Benefit Summary =====\n\n")

    f.write("Part 1 — Loan Cost\n")
    f.write(f"Section D: ${result['Section D(Sum)']:,.2f}\n")
    f.write(f"Total Cost: ${result['Total Cost of Loan']:,.2f}\n")
    f.write(f"Benefit: ${result['Benefits']:,.2f}\n\n")

    f.write("Part 2 — Escrow & Payoff\n")
    f.write(f"Excess: ${result2['Excess Amount over Payoff']:,.2f}\n")
    f.write(f"Escrow + Prepaid: ${result2['Escrows + Prepaid']:,.2f}\n")
    f.write(f"Final Benefit: ${result2['Benefits']:,.2f}\n")

# JSON OUTPUT
with open("outputs/output.json", "w") as f:
    json.dump({
        "part1": result,
        "part2": result2
    }, f, indent=4)