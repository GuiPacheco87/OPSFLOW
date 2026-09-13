def auth(client):
    r=client.post("/api/v1/auth/register",json={"organization_name":"Acme","name":"Ana","email":"ana@acme.com","password":"segredo123"})
    assert r.status_code==201
    return {"Authorization":f"Bearer {r.json()['access_token']}"}
def test_registration_and_workflow_execution(client):
    h=auth(client)
    assert client.get("/api/v1/me",headers=h).json()["role"]=="admin"
    w=client.post("/api/v1/workflows",headers=h,json={"name":"Onboarding","status":"active"}).json()
    assert client.post(f"/api/v1/workflows/{w['id']}/steps",headers=h,json={"name":"Gestor aprova","order":1,"assigned_role":"manager"}).status_code==201
    assert client.post("/api/v1/executions",headers=h,json={"workflow_id":w["id"],"request_data":{"name":"João"}}).status_code==201
    assert client.get("/api/v1/tasks",headers=h).json()[0]["status"]=="pending"
def test_inactive_workflow_is_blocked(client):
    h=auth(client); w=client.post("/api/v1/workflows",headers=h,json={"name":"Rascunho"}).json()
    assert client.post("/api/v1/executions",headers=h,json={"workflow_id":w["id"]}).status_code==409

