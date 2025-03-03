def test_register(client):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "username": "testuser2",
            "email": "testuser2@example.com",
            "password": "password123"
        }
    )
    print("\n[REGISTER] Status:", response.status_code)
    print("[REGISTER] Response:", response.json())
    assert response.status_code == 200
    assert response.json()["email"] == "testuser2@example.com"


def test_login(client):
    client.post(
        "/api/v1/auth/register",
        json={
            "username": "testuser3",
            "email": "testuser3@example.com",
            "password": "password123"
        }
    )
    
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "testuser3@example.com",
            "password": "password123"
        }
    )
    print("\n[LOGIN] Status:", response.status_code)
    print("[LOGIN] Response:", response.json())
    assert response.status_code == 200
    assert "access_token" in response.json()
