def get_auth_token(client):

    register_payload = {
        "email": "testuser@gmail.com",
        "password": "testuser123"
    }

    client.post("/auth/register", json=register_payload)

    login_payload = {
        "username": "testuser@gmail.com",
        "password": "testuser123"
    }

    response = client.post(
        "/auth/login",
        data=login_payload
    )

    return response.json()["access_token"]

def test_create_patients_returns_201(client):

    token = get_auth_token(client)

    payload = {
        "name": "testuser",
        "blood_group": "B+",
        "age": 19,
        "contact": "987654"
    }

    response = client.post(
        "/patients",
        json=payload,
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code in [200, 201]