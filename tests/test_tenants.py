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
    tenant = client.post("/tenant/register", json={"name":"Test sd"},
                              headers={"Authorization":f"Bearer {create_user["first_token"]}"})
    assert tenant.status_code == 500

def test_creation_to_not_work_due_not_exist_status(client,create_user):
    with sync_engine.begin() as conn:
        conn.execute(models.StatusDB.__table__.delete())
    tenant = client.post("/tenant/register", json={"name":"Test sd"},
                              headers={"Authorization":f"Bearer {create_user["first_token"]}"})
    assert tenant.status_code == 500

