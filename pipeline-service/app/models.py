from sqlalchemy import Column, Integer, String, Float, DateTime
from .database import Base

class Customer(Base):
    __tablename__ = "customers"

    customer_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    phone = Column(String)
    address = Column(String)
    date_of_birth = Column(String)
    account_balance = Column(Float)
    created_at = Column(DateTime)