def test_home_endpoint_returns_200(client):
    response = client.get('/')

    assert response.status_code == 200
    assert "message" in response.json()

def test_health_endpoints_returns_200(client):
    response = client.get('/health')

    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_health_contains_version(client):
    response = client.get("/health")

    assert "version" in response.json()