from pydantic import BaseModel
from datetime import datetime

class CustomerBase(BaseModel):
    customer_id: int
    first_name: str
    last_name: str
    email: str
    phone: str
    address: str
    date_of_birth: str
    account_balance: float
    created_at: datetime

    class Config:
        from_attributes = True