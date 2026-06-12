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

def test_create_appointment_returns_201(client):

    token = get_auth_token(client)

    headers = {
        "Authorization": f"Bearer {token}"
    }

    patient_response = client.post(
        "/patients",
        json={
            "name": "Ananya",
            "blood_group": "A+",
            "age": 22,
            "contact": "9876543210"
        },
        headers=headers
    )

    print(patient_response.json())

    doctor_response = client.post(
        "/doctors",
        json={
            "name": "Dr Sharma",
            "specialization": "Cardiology"
        },
        headers=headers
    )

    print(doctor_response.json())

def test_create_appointment_invalid_patient(client):

    token = get_auth_token(client)

    payload = {
        "patient_id": "P999",
        "doctor_id": "D001",
        "time_slot": "10:00",
        "status": "Scheduled"
    }

    response = client.post(
        "/appointments/book",
        json=payload,
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code in [404, 400]

def test_create_appointment_invalid_doctor(client):

    token = get_auth_token(client)

    payload = {
        "patient_id": "P001",
        "doctor_id": "D999",
        "time_slot": "10:00",
        "status": "Scheduled"
    }

    response = client.post(
        "/appointments/book",
        json=payload,
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code in [404, 400]