import os
from fastapi import FastAPI, Depends, HTTPException, status, Header
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, Float, ForeignKey, TIMESTAMP, select
from starlette.status import HTTP_401_UNAUTHORIZED
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql+asyncpg://postgres:password@localhost/demo_db")
API_KEY = os.environ.get("API_KEY", "mysecretkey")

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)
Base = declarative_base()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class Customer(Base):
    __tablename__ = "customers"
    id = Column(String, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    phone = Column(String)
    join_date = Column(TIMESTAMP)

class Card(Base):
    __tablename__ = "cards"
    id = Column(String, primary_key=True)
    type = Column(String)
    status = Column(String)
    balance = Column(Float)
    issue_date = Column(TIMESTAMP)
    customer_id = Column(String, ForeignKey("customers.id"))

class Case(Base):
    __tablename__ = "cases"
    id = Column(String, primary_key=True)
    customer_id = Column(String, ForeignKey("customers.id"))
    type = Column(String)
    status = Column(String)
    priority = Column(String)
    assigned_to = Column(String)
    created_at = Column(TIMESTAMP)

class Trip(Base):
    __tablename__ = "trips"
    id = Column(String, primary_key=True)
    card_id = Column(String, ForeignKey("cards.id"))
    station = Column(String)
    type = Column(String)
    amount = Column(Float)
    status = Column(String)
    timestamp = Column(TIMESTAMP)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

async def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid API Key")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
@app.post("/customers/", dependencies=[Depends(verify_api_key)])
async def create_customer(id: str, name: str, email: str, phone: str, join_date: str, db: AsyncSession = Depends(get_db)):
    try:
        join_date_obj = datetime.strptime(join_date, "%Y-%m-%d")
    except Exception:
        raise HTTPException(status_code=400, detail="join_date must be in YYYY-MM-DD format")
    customer = Customer(id=id, name=name, email=email, phone=phone, join_date=join_date_obj)
    db.add(customer)
    await db.commit()
    await db.refresh(customer)
    return customer

@app.get("/customers/", dependencies=[Depends(verify_api_key)])
async def read_customers(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Customer))
    return result.scalars().all()

@app.get("/customers/{customer_id}", dependencies=[Depends(verify_api_key)])
async def read_customer(customer_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Customer).where(Customer.id == customer_id))
    customer = result.scalar_one_or_none()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@app.delete("/customers/{customer_id}", dependencies=[Depends(verify_api_key)])
async def delete_customer(customer_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Customer).where(Customer.id == customer_id))
    customer = result.scalar_one_or_none()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    await db.delete(customer)
    await db.commit()
    return {"ok": True}

@app.post("/cards/", dependencies=[Depends(verify_api_key)])
async def create_card(id: str, type: str, status: str, balance: float, issue_date: str, customer_id: str, db: AsyncSession = Depends(get_db)):
    try:
        issue_date_obj = datetime.strptime(issue_date, "%Y-%m-%d")
    except Exception:
        raise HTTPException(status_code=400, detail="issue_date must be in YYYY-MM-DD format")
    card = Card(id=id, type=type, status=status, balance=balance, issue_date=issue_date_obj, customer_id=customer_id)
    db.add(card)
    await db.commit()
    await db.refresh(card)
    return card

@app.get("/cards/", dependencies=[Depends(verify_api_key)])
async def read_cards(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Card))
    return result.scalars().all()

@app.get("/cards/{card_id}", dependencies=[Depends(verify_api_key)])
async def read_card(card_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Card).where(Card.id == card_id))
    card = result.scalar_one_or_none()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    return card

@app.delete("/cards/{card_id}", dependencies=[Depends(verify_api_key)])
async def delete_card(card_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Card).where(Card.id == card_id))
    card = result.scalar_one_or_none()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    await db.delete(card)
    await db.commit()
    return {"ok": True}

@app.post("/cases/", dependencies=[Depends(verify_api_key)])
async def create_case(id: str, customer_id: str, type: str, status: str, priority: str, assigned_to: str, created_at: str, db: AsyncSession = Depends(get_db)):
    try:
        created_at_obj = datetime.strptime(created_at, "%Y-%m-%d")
    except Exception:
        raise HTTPException(status_code=400, detail="created_at must be in YYYY-MM-DD format")
    case = Case(id=id, customer_id=customer_id, type=type, status=status, priority=priority, assigned_to=assigned_to, created_at=created_at_obj)
    db.add(case)
    await db.commit()
    await db.refresh(case)
    return case

@app.get("/cases/", dependencies=[Depends(verify_api_key)])
async def read_cases(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Case))
    return result.scalars().all()

@app.get("/cases/{case_id}", dependencies=[Depends(verify_api_key)])
async def read_case(case_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Case).where(Case.id == case_id))
    case = result.scalar_one_or_none()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return case

@app.delete("/cases/{case_id}", dependencies=[Depends(verify_api_key)])
async def delete_case(case_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Case).where(Case.id == case_id))
    case = result.scalar_one_or_none()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    await db.delete(case)
    await db.commit()
    return {"ok": True}

@app.post("/trips/", dependencies=[Depends(verify_api_key)])
async def create_trip(id: str, card_id: str, station: str, type: str, amount: float, status: str, timestamp: str, db: AsyncSession = Depends(get_db)):
    try:
        timestamp_obj = datetime.strptime(timestamp, "%Y-%m-%d")
    except Exception:
        raise HTTPException(status_code=400, detail="timestamp must be in YYYY-MM-DD format")
    trip = Trip(id=id, card_id=card_id, station=station, type=type, amount=amount, status=status, timestamp=timestamp_obj)
    db.add(trip)
    await db.commit()
    await db.refresh(trip)
    return trip

@app.get("/trips/", dependencies=[Depends(verify_api_key)])
async def read_trips(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Trip))
    return result.scalars().all()

@app.get("/trips/{trip_id}", dependencies=[Depends(verify_api_key)])
async def read_trip(trip_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Trip).where(Trip.id == trip_id))
    trip = result.scalar_one_or_none()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    return trip

@app.delete("/trips/{trip_id}", dependencies=[Depends(verify_api_key)])
async def delete_trip(trip_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Trip).where(Trip.id == trip_id))
    trip = result.scalar_one_or_none()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    await db.delete(trip)
    await db.commit()
    return {"ok": True} 
