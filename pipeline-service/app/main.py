from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError
import time

from .database import SessionLocal, engine, Base
from . import crud, models
from .services.ingestion import fetch_all_customers

app = FastAPI()


# ✅ Proper DB wait logic (production-style)
def wait_for_db(max_retries=10, delay=2):
    for attempt in range(max_retries):
        try:
            conn = engine.connect()
            conn.close()
            print("Database connected")
            return
        except OperationalError:
            print(f"DB not ready... retrying ({attempt+1}/{max_retries})")
            time.sleep(delay)

    raise Exception("Could not connect to database after retries")


# ✅ Run at startup
@app.on_event("startup")
def startup():
    wait_for_db()
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/api/ingest")
def ingest(db: Session = Depends(get_db)):
    try:
        customers = fetch_all_customers()

        for c in customers:
            crud.upsert_customer(db, c)

        return {
            "status": "success",
            "records_processed": len(customers)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/customers")
def get_customers(page: int = 1, limit: int = 10, db: Session = Depends(get_db)):
    offset = (page - 1) * limit

    data = db.query(models.Customer).offset(offset).limit(limit).all()
    total = db.query(models.Customer).count()

    return {
        "data": data,
        "total": total,
        "page": page,
        "limit": limit
    }


@app.get("/api/customers/{customer_id}")
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(models.Customer).filter(
        models.Customer.customer_id == customer_id
    ).first()

    if not customer:
        raise HTTPException(status_code=404, detail="Not found")

    return customer