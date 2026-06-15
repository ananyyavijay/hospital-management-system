# tests/test_admin.py
#

def get_auth_token(client, email, password, role):

    register_payload = {
        "email": email,
        "password": password,
        "role": role
    }

    client.post(
        "/auth/register",
        json=register_payload
    )

    login_response = client.post(
        "/auth/login",
        data={
            "username": email,
            "password": password
        }
    )

    return login_response.json()["access_token"]


def test_patient_cannot_access_admin_patients(client):

    token = get_auth_token(
        client,
        "patient403@gmail.com",
        "test123",
        "patient"
    )

    response = client.get(
        "/admin/admin/patients",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 403


def test_admin_can_access_admin_patients(client):

    token = get_auth_token(
        client,
        "admin403@gmail.com",
        "test123",
        "admin"
    )

    response = client.get(
        "/admin/admin/patients",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200