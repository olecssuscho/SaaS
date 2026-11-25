from datetime import datetime, timezone
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.pool import NullPool
from database import Base
from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker
from sqlalchemy import create_engine, insert
from depends import get_db
from main import app
import models

TEST_DATABASE_URL_ASYNC = "postgresql+asyncpg://postgres:123qwe@localhost:5432/SaaS_DB_Test"
TEST_DATABASE_URL_SYNC = "postgresql+psycopg2://postgres:123qwe@localhost:5432/SaaS_DB_Test"

async_engine = create_async_engine(TEST_DATABASE_URL_ASYNC,poolclass=NullPool)
Async_Session = async_sessionmaker(async_engine)

sync_engine = create_engine(TEST_DATABASE_URL_SYNC)

async def override_db():
    async with Async_Session() as db:
        yield db

@pytest.fixture(scope="session",autouse=True)
def prepare_tables():
    now = datetime.now(timezone.utc)
    Base.metadata.create_all(bind=sync_engine)
    with sync_engine.begin() as conn:
        conn.execute(insert(models.PlanDB).values(name ="Free",price_cents = 0,max_links = 50,max_clicks_per_month=1000,max_members = 1,analytics_retention_days = 30,allow_custom_domain = False,allow_api = False,is_active=True,period_days = None,created_at = now))
        conn.execute(insert(models.PlanDB).values(name ="Pro", price_cents = 900,max_links = 1000,max_clicks_per_month=50000,max_members = 5,analytics_retention_days = 365,allow_custom_domain = True,allow_api = True,is_active=True,period_days = 365,created_at =now))
        # add Status for test DB 
        conn.execute(insert(models.StatusDB).values(name = "active",description = "Subscription is active"))
        conn.execute(insert(models.StatusDB).values(name = "trial",description = "Trial period"))
        conn.execute(insert(models.StatusDB).values(name = "past_due",description = "Payment failed, grace period"))
        conn.execute(insert(models.StatusDB).values(name = "canceled",description = "Canceled, active until periodend"))
        conn.execute(insert(models.StatusDB).values(name = "expired",description = "Period ended, free limits apply"))
    yield
    Base.metadata.drop_all(bind=sync_engine)

KEEP_TABLE=[models.PlanDB.__table__,models.StatusDB.__table__]

@pytest.fixture(autouse=True)
def clean_tables():
    yield
    with sync_engine.begin() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            if table not in KEEP_TABLE:
                conn.execute(table.delete())

@pytest.fixture(scope="session")
def client():
    app.dependency_overrides[get_db] = override_db
    with TestClient(app) as c:
        yield c 

@pytest.fixture(autouse=True)
def create_user(client):
    # now it will be one but futher at least 3 
    client.post("/user/register", json={"email": "owner@test.com", "password": "Mass#12345", "fullname": "Owner"})

    first = client.post("/user/login", data={"username": "owner@test.com", "password": "Mass#12345"})

    first_token = first.json()["access_token"]

    return {"first_token": first_token}
