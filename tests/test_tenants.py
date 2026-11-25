from datetime import datetime, timezone
from sqlalchemy import insert, select
from unittest.mock import patch
from sqlalchemy.exc import SQLAlchemyError
from conftest import sync_engine
import models

def test_creation_work_correct(client,create_user):
    tenant = client.post("/tenant/register", json={"name":"Test sd"},
                          headers={"Authorization":f"Bearer {create_user["first_token"]}"})
    assert tenant.status_code == 200

def test_creation_do_not_work_due_to_non_exist_token(client):
    tenant = client.post("/tenant/register", json={"name":"Test sd"},
                          headers={"Authorization":f"Bearer ss"})
    assert tenant.status_code == 401

def test_creation_do_not_work_due_to_exist_company(client,create_user):
    tenant = client.post("/tenant/register", json={"name":"Test sd"},
                          headers={"Authorization":f"Bearer {create_user["first_token"]}"})
    assert tenant.status_code == 200   
    tenant_2 = client.post("/tenant/register", json={"name":"Test sd"},
                          headers={"Authorization":f"Bearer {create_user["first_token"]}"})
    assert tenant_2.status_code == 409

def test_creation_to_not_work_due_not_exist_plan(client,create_user):
    with sync_engine.begin() as conn:
        conn.execute(models.PlanDB.__table__.delete())
    try:
        tenant = client.post("/tenant/register", json={"name":"Test sd"},
                                  headers={"Authorization":f"Bearer {create_user["first_token"]}"})
        assert tenant.status_code == 500
    finally:
        now = datetime.now(timezone.utc)
        with sync_engine.begin() as conn:
            conn.execute(insert(models.PlanDB).values(name ="Free",price_cents = 0,max_links = 50,max_clicks_per_month=1000,max_members = 1,analytics_retention_days = 30,allow_custom_domain = False,allow_api = False,is_active=True,period_days = None,created_at = now))
            conn.execute(insert(models.PlanDB).values(name ="Pro", price_cents = 900,max_links = 1000,max_clicks_per_month=5000, max_members = 5,analytics_retention_days = 365,allow_custom_domain = True,allow_api = True,is_active=True,period_days = 365,created_at =now))
        

def test_creation_to_not_work_due_not_exist_status(client,create_user):
    with sync_engine.begin() as conn:
        conn.execute(models.StatusDB.__table__.delete())
    try:
        tenant = client.post("/tenant/register", json={"name":"Test sd"},
                                  headers={"Authorization":f"Bearer {create_user["first_token"]}"})
        assert tenant.status_code == 500
    finally:
        with sync_engine.begin() as conn:
            conn.execute(insert(models.StatusDB).values(name = "active",description = "Subscription is active"))
            conn.execute(insert(models.StatusDB).values(name = "trial",description = "Trial period"))
            conn.execute(insert(models.StatusDB).values(name = "past_due",description = "Payment failed, grace period"))
            conn.execute(insert(models.StatusDB).values(name = "canceled",description = "Canceled, active until periodend"))
            conn.execute(insert(models.StatusDB).values(name = "expired",description = "Period ended, free limits apply"))

def test_exception(client,create_user):
    with patch("services.tenants.AsyncSession.commit",side_effect=SQLAlchemyError(".")):
        tenant = client.post("/tenant/register", json={"name":"Test sd"},
                              headers={"Authorization":f"Bearer {create_user["first_token"]}"})
    assert tenant.status_code == 415

    with sync_engine.begin() as conn:
        res_tenants = conn.execute(select(models.TenantDB))
        res_member = conn.execute(select(models.TenantMembershipDB))
        res_tenants_list=[]
        res_member_list=[]
        for i in res_tenants:
            res_tenants_list.append(i)
        for i in res_member:
            res_member_list.append(i)
        
    assert len(res_tenants_list)==0
    assert len(res_member_list)==0
