def calculate_part1(data):
    A = data["A"]
    B = data["B"]
    C = data["C"]
    E = data["E"]
    J = data["J"]

    D = A + B + C
    Total_Cost = D + E
    Benefit = Total_Cost + J

    return {
        "Section D(Sum)": round(D,2),
        "Total Cost of Loan": round(Total_Cost,2),
        "Benefits": round(Benefit,2)
    }

## ------------------------------------------------------
## Part 2: Calculation

def calculate_part2(part2_data):
    loan = part2_data["loan"]
    payoff = part2_data["payoff"]
    principal = part2_data["principal"]
    prepaid = part2_data["prepaid"]
    escrow = part2_data["escrow"]
    cash_to_close = part2_data["cash"]

    excess = payoff + principal - loan # excess payoff amount
    total= prepaid + escrow  ## total of prepaid + escrow
    total_2 = excess + total # total of prepaid + escrow + excess payoff
    benefit = total_2 - cash_to_close # benefit to borrower
    
    return {
        "Excess Amount over Payoff": round(excess, 2),
        "Escrows + Prepaid": round(total, 2),
        "Escrows + Prepaid + Excess Payoff": round(total_2, 2),
        "Benefits": round(benefit, 2)
    }
