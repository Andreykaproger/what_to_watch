

def test_get_list_opinions_api(client):

    response = client.get("/api/opinions")

    assert response.status_code == 200


def test_create_opinion_api(client, auth_tokens):

    response = client.post(
        "/api/opinions/create",
        json={
            "title": "API opinion",
            "text": "API Text opinion",
            "source": "API source"
        },
        headers={
            "Authorization": f"Bearer {auth_tokens["access_token"]}"
        }
    )

    assert response.status_code == 200
    assert response.json["title"] == "API opinion"

    from opinions_app.models import Opinion

    opinions = Opinion.query.first()

    assert opinions


def test_update_opinion_api(client, auth_tokens, opinion):

    new_data = {
        "title": "Updated API opinion",
        "text": "Updated API Text opinion"
    }

    response = client.patch(
        f"/api/opinions/{opinion.id}",
        json = new_data,
        headers = {
            "Authorization": f"Bearer {auth_tokens["access_token"]}"
        }
    )

    data = response.json

    assert response.status_code == 200
    assert data["title"] == "Updated API opinion"
    assert data["text"] == "Updated API Text opinion"

    from opinions_app.models import Opinion, OpinionStatus

    updated = Opinion.query.get_or_404(opinion.id)

    assert updated.title == "Updated API opinion"
    assert updated.text == "Updated API Text opinion"
    assert updated.status == OpinionStatus.PENDING


def test_delete_opinion_api(client, auth_tokens, opinion):

    response = client.delete(
        f"/api/opinions/{opinion.id}",
        headers = {
            "Authorization": f"Bearer {auth_tokens["access_token"]}"
        }
    )

    assert response.status_code == 204

