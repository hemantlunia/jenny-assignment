from sqlalchemy.orm import Session
from .models import Customer

def upsert_customer(db: Session, data: dict):
    customer = db.query(Customer).filter(
        Customer.customer_id == data["customer_id"]
    ).first()

    if customer:
        for key, value in data.items():
            setattr(customer, key, value)
    else:
        customer = Customer(**data)
        db.add(customer)

    db.commit()