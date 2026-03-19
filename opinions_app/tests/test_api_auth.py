

def test_api_register(client):

    response = client.post(
        "/api/auth/register",
        json={
            "username": "newuser",
            "email": "new@new.com",
            "password": "password"
        }
    )

    assert response.status_code == 200
    assert response.json["message"] == "Пользователь успешно зарегистрирован"


def test_api_login(client, user):

    response = client.post(
        "api/auth/login",
        json={
            "email": user.email,
            "password": "password"
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.json
    assert "refresh_token" in response.json


def test_login_wrong_password(client):

    response = client.post(
        "api/auth/login",
        json={
            "email": "new@new.com",
            "password": "wrong_password"
        }
    )

    assert response.status_code == 400
    assert response.json["message"] == "Неверный E-mail или пароль"


def test_blocked_user_login(client, blocked_user):

    response = client.post(
        "api/auth/login",
        json={
            "email": blocked_user.email,
            "password": "password"
        }
    )

    assert response.status_code == 403
    assert "message" in response.json


def test_api_logout(client, auth_tokens):
    response = client.post(
        "api/auth/logout",
        headers = {
            "Authorization": f"Bearer {auth_tokens["access_token"]}"
        }
    )

    assert response.status_code == 200
    assert "message" in response.json


def test_refresh_token(client, auth_tokens):

    response = client.post(
        "/api/auth/refresh",
        headers={
            "Authorization": f"Bearer {auth_tokens["refresh_token"]}"
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.json


def test_access_without_token(client):

    response = client.get(
        "/api/auth/profile"
    )

    data = response.json

    assert response.status_code == 401
    assert "msg" in data or "message" in data


def test_access_with_invalid_token(client):

    response = client.get(
        "/api/auth/profile",
        headers= {
            "Authorization": "Bearer invalid_token"
        }
    )

    assert response.status_code == 422


