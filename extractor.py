import re
##  Part 1: Extracting Specific Values

def extract_value(text, keyword):
    lines = text.split("\n")

    for line in lines:
        if keyword in line:
            match = re.search(r"-?\$[\d,]+\.\d{2}", line)
            if match:
                value = match.group()
                value=value.replace("$", "").replace(",", "")
                return float(value)

    return 0.0


 ##  Part 2:
 ##--------------------------------------------------------
 ##  Extracting Payoff Amounts

def extract_payoff_amount(text):
    total = 0.0
    lines = text.split("\n")
    capture = False

    for i,line in enumerate(lines):
        if "Payoffs and Payments" in line:
            capture = True
            continue

        if capture:
            if "Principal Reduction" in line:
                break

            if "Payoff to" in line:
                match = re.search(r"-?\$[\d,]+\.\d{2}", lines[i+1])
                if match:
                    value = match.group()
                    cleaned = value.replace("$", "").replace(",", "")
                    total += float(cleaned)

    return round(total, 2)

##------------------------------------------------------
## Principal Reduction Extraction

def extract_principal_reduction(text):
    lines = text.split("\n")
    capture = False

    for i, line in enumerate(lines):
        if "Payoffs and Payments" in line:
            capture = True
            continue

        if capture:
            if "Principal Reduction" in line:
                match = re.search(r"-?\$[\d,]+\.\d{2}", lines[i+1])
                if match:
                    value = match.group()
                    cleaned = value.replace("$", "").replace(",", "")
                    return float(cleaned)

    return 0.0

##------------------------------------------------------
## Loan Amount Extraction

def extract_loan_amount(text):
    lines = text.split("\n")

    for line in lines:
        if "Loan Amount" in line:
            match = re.search(r"-?\$[\d,]+\.\d{2}", line)
            if match:
                value = match.group()
                cleaned = value.replace("$", "").replace(",", "")
                return float(cleaned)

    return 0.0

##------------------------------------------------------
## Prepaid Extraction

def extract_prepaid(text):
    lines = text.split("\n")
    total = 0.0
    capture = False

    for line in lines:
        if "F. Prepaids" in line:
            capture = True
            continue

        if capture:
            if "G. Initial Escrow" in line:
                break

            if "Prepaid Interest" in line or "Homeowner" in line:
                match = re.findall(r"-?\$[\d,]+\.\d{2}", line)
                if match:
                    cleaned = match[-1].replace("$", "").replace(",", "")
                    total += float(cleaned)

    return round(total, 2)

##------------------------------------------------------
## Escrow Extraction

def extract_escrow(text):
    lines = text.split("\n")
    total = 0.0
    capture = False

    for line in lines:
        if "G. Initial Escrow" in line:
            capture = True
            continue

        if capture:
            if "H. Other" in line:
                break
            if "Initial Escrow Payment" in line:
                continue

            matches = re.findall(r"-?\$[\d,]+\.\d{2}", line)
            if matches:
              cleaned = matches[-1].replace("$", "").replace(",", "")
              total += float(cleaned)

    return round(total, 2)

##------------------------------------------------------
## Cash to Close Extraction


def extract_cash_to_close(text):
    lines = text.split("\n")

    for i, line in enumerate(lines):
        if "cash to close" in line.lower():
            if i > 0:
                prev_line = lines[i-1]
                match = re.search(r"-?\$[\d,]+\.\d{2}", prev_line)
                if match:
                    value = match.group()
                    cleaned = value.replace("$", "").replace(",", "")
                    return float(cleaned)

    return 0.0


