def test_creation_work_correct(client,create_user):
    tenant = client.post("/tenant/register", json={"name":"Test sd","plane_name":"Free"},
                          headers={"Authorization":f"Bearer {create_user["first_token"]}"})
    assert tenant.status_code == 200

def test_creation_do_not_work_due_to_non_exist_token(client):
    tenant = client.post("/tenant/register", json={"name":"Test sd","plane_name":"Free"},
                          headers={"Authorization":f"Bearer ss"})
    assert tenant.status_code == 401