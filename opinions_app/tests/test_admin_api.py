

def test_admin_block_user(client, admin_auth_tokens, user):

    response = client.post(
        f"/api/admin/users/{user.id}/block",
        json = {
            "reason": "Test block user"
        },
        headers = {
            "Authorization": f"Bearer {admin_auth_tokens["access_token"]}"
        }
    )

    assert response.status_code == 200
    assert "message" in response.json

def test_admin_unblock_user(client, blocked_user, admin_auth_tokens):

    response = client.post(
        f"/api/admin/users/{blocked_user.id}/unblock",
        headers={
            "Authorization": f"Bearer {admin_auth_tokens["access_token"]}"
        }
    )

    assert response.status_code == 200
    assert "message" in response.json


def test_admin_reject_opinion(client, admin_auth_tokens, pending_opinion):

    response = client.post(
        f"api/admin/opinions/{pending_opinion.id}/reject",
        json={
            "reason": "test reject opinion"
        },
        headers = {
            "Authorization": f"Bearer {admin_auth_tokens["access_token"]}"
        }
    )

    assert response.status_code == 200
    assert "message" in response.json


def test_admin_approve_opinion(client, admin_auth_tokens, pending_opinion):

    response = client.post(
        f"api/admin/opinions/{pending_opinion.id}/approve",
        headers = {
            "Authorization": f"Bearer {admin_auth_tokens["access_token"]}"
        }
    )

    assert response.status_code == 200
    assert "message" in response.json


def test_admin_reject_approved_opinion(client, admin_auth_tokens, opinion):

    response = client.post(
        f"api/admin/opinions/{opinion.id}/reject",
        json={
            "reason": "Test reject"
        },
        headers = {
            "Authorization": f"Bearer {admin_auth_tokens["access_token"]}"
        }
    )

    assert response.status_code == 400
