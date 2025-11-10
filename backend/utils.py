import csv
from io import StringIO

EXPECTED = [
    "Invoice_date","Invoice_Number","Payment_date",
    "Company_Name","Supplier_Name","Invoice_Amount","Amount_Paid"
]

def _num(x):
    try: return float(x)
    except: return 0.0

def read_csv_text_to_rows(text: str):
    f = StringIO(text)
    reader = csv.DictReader(f)
    if not reader.fieldnames:
        raise ValueError("CSV seems empty or has no header")
    missing = [h for h in EXPECTED if h not in reader.fieldnames]
    if missing:
        raise ValueError("Missing headers: " + ", ".join(missing))
    out = []
    for r in reader:
        if not any(r.values()):
            continue
        row = {k: (r.get(k,"") or "").strip() for k in EXPECTED}
        row["Company_Name"]  = row["Company_Name"].upper()
        row["Supplier_Name"] = row["Supplier_Name"].upper()
        row["Invoice_Amount"] = _num(row["Invoice_Amount"])
        row["Amount_Paid"]    = _num(row["Amount_Paid"])
        out.append(row)
    return out
