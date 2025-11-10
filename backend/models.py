from sqlalchemy import Column, Integer, String, Float
from .database import Base

class PaymentRow(Base):
    __tablename__ = "payments"
    id = Column(Integer, primary_key=True, index=True)
    Invoice_date = Column(String, nullable=True)
    Invoice_Number = Column(String, index=True)
    Payment_date = Column(String, nullable=True)
    Company_Name = Column(String, index=True)
    Supplier_Name = Column(String, index=True)
    Invoice_Amount = Column(Float, default=0.0)
    Amount_Paid = Column(Float, default=0.0)
