# backend/app.py
from pathlib import Path
from typing import List

from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .models import PaymentRow
from .schemas import PaymentRowOut, UploadResult
from .utils import read_csv_text_to_rows

app = FastAPI(title="Payments Backend", version="1.0.0")

# DB tables
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

# API: health
@app.get("/health")
def health():
    return {"ok": True}

# API: upload CSV → store rows in DB
@app.post("/upload-csv", response_model=UploadResult)
async def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Please upload a .csv file.")
    content = (await file.read()).decode("utf-8", errors="ignore")
    try:
        rows = read_csv_text_to_rows(content)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    inserted, replaced = 0, 0
    for r in rows:
        q = (
            db.query(PaymentRow)
            .filter(
                PaymentRow.Invoice_Number == r["Invoice_Number"],
                PaymentRow.Company_Name == r["Company_Name"],
                PaymentRow.Supplier_Name == r["Supplier_Name"],
                PaymentRow.Payment_date == r["Payment_date"],
                PaymentRow.Invoice_date == r["Invoice_date"],
            )
        )
        existing = q.first()
        if existing:
            existing.Invoice_Amount = r["Invoice_Amount"]
            existing.Amount_Paid = r["Amount_Paid"]
            db.add(existing)
            replaced += 1
        else:
            db.add(PaymentRow(**r))
            inserted += 1

    db.commit()
    total = db.query(PaymentRow).count()
    return {"inserted": inserted, "replaced": replaced, "total_rows_in_db": total}

# API: fetch all rows (frontend aggregates same as before)
@app.get("/feedback", response_model=List[PaymentRowOut])
def get_feedback(db: Session = Depends(get_db)):
    return db.query(PaymentRow).order_by(PaymentRow.id.asc()).all()

# ---- Static site (serve your index.html) ----
static_dir = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Root: return the SPA (index.html)
@app.get("/")
def spa_root():
    return FileResponse(static_dir / "index.html")
