def test_register_user_returns_success(client):
    payload = {
        "email" : "testuser@gmail.com",
        "password" : "testuser123",
        "role" : "patient"
    }

    response = client.post("/auth/register", json=payload)
    assert response.status_code in [200, 201]

def test_login_returns(client):
    register_payload = {
    "email": "testuser@gmail.com",
    "password": "testuser123"
    }

    client.post("/auth/register", json=register_payload)

    login_payload = {
    "username": "testuser@gmail.com",
    "password": "testuser123"
    }

    response = client.post("/auth/login", data=login_payload)

    assert response.status_code == 200
    assert "access_token" in response.json()