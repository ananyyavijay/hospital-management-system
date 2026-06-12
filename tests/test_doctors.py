def get_auth_token(client):

    register_payload = {
        "email": "testdoc@gmail.com",
        "password": "testdoc123"
    }

    client.post("/auth/register", json=register_payload)

    login_payload = {
        "username": "testdoc@gmail.com",
        "password": "testdoc123"
    }

    response = client.post(
        "/auth/login",
        data=login_payload
    )

    return response.json()["access_token"]

def test_create_doctor_returns_201(client):

    token = get_auth_token(client)

    payload = {
        "name": "testdoc",
        "specialization": "test"
}

    response = client.post(
        "/doctors",
        json=payload,
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code in [200, 201]