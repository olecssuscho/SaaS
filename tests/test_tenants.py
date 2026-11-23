def test_creation_work_good(client,create_user):
    tenant = client.post("/tenant/register", json={"name":"Test sd","plane_name":"Free"},
                          headers={"Authorization":f"Bearer {create_user["first_token"]}"})
    assert tenant.status_code == 200