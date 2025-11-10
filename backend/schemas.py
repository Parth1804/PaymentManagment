from pydantic import BaseModel
from typing import Optional

class PaymentRowOut(BaseModel):
    id: int
    Invoice_date: Optional[str]
    Invoice_Number: str
    Payment_date: Optional[str]
    Company_Name: str
    Supplier_Name: str
    Invoice_Amount: float
    Amount_Paid: float

    class Config:
        from_attributes = True

class UploadResult(BaseModel):
    inserted: int
    replaced: int
    total_rows_in_db: int
