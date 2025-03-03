def test_summarize(client):
    # Registrar el usuario
    client.post(
        "/api/v1/auth/register",
        json={
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "password123"
        }
    )

    login_response = client.post(
        "/api/v1/auth/login",
        data={"username": "testuser@example.com", "password": "password123"}
    )

    assert login_response.status_code == 200, login_response.text
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # ✅ Crear un documento
    upload_response = client.post(
        "/api/v1/documents/upload",
        headers=headers,
        files={"file": ("test_document.txt", b"Este es el contenido del documento.", "text/plain")}
    )
    assert upload_response.status_code == 200, upload_response.text
    document_id = upload_response.json()["id"]

    # ✅ Ahora sí usamos el documento creado
    response = client.get(f"/api/v1/analysis/summarize/{document_id}", headers=headers)
    print("\n[SUMMARIZE] Status:", response.status_code)
    print("[SUMMARIZE] Response:", response.json())
    assert response.status_code == 200, response.text

def test_ask(client):
    # Registrar el usuario
    client.post(
        "/api/v1/auth/register",
        json={
            "username": "testuser1",
            "email": "testuser1@example.com",
            "password": "password123"
        }
    )

    login_response = client.post(
        "/api/v1/auth/login",
        data={"username": "testuser1@example.com", "password": "password123"}
    )
    assert login_response.status_code == 200, login_response.text
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # ✅ Crear un documento
    upload_response = client.post(
        "/api/v1/documents/upload",
        headers=headers,
        files={"file": ("test_document.txt", b"Este es el contenido del documento.", "text/plain")}
    )
    assert upload_response.status_code == 200, upload_response.text
    document_id = upload_response.json()["id"]

    # ✅ Ahora hacemos la pregunta
    response = client.post(
        f"/api/v1/analysis/ask/{document_id}",
        headers=headers,
        params={"question": "¿De qué trata el documento?"}
    )
    print("\n[ASK] Status:", response.status_code)
    print("[ASK] Response:", response.json())
    assert response.status_code == 200, response.text
    assert "answer" in response.json()
