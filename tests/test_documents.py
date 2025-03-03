def test_upload_document(client):
    # Primero hacemos login para obtener el token
    login_response = client.post(
        "/api/v1/auth/login",
        data={"username": "testuser@example.com", "password": "password123"}
    )
    token = login_response.json()["access_token"]

    with open("tests/files/test_document.txt", "w") as f:
        f.write("Este es un documento de prueba.")

    with open("tests/files/test_document.txt", "rb") as file:
        response = client.post(
            "/api/v1/documents/upload",
            headers={"Authorization": f"Bearer {token}"},
            files={"file": ("test_document.txt", file, "text/plain")}
        )
    print("\n[UPLOAD DOCUMENT] Status:", response.status_code)
    print("[UPLOAD DOCUMENT] Response:", response.json())
    assert response.status_code == 200
    assert response.json()["title"] == "test_document.txt"
