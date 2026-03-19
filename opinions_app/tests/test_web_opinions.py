

def test_index_page(client):
    response = client.get('/')

    assert response.status_code in (200,404)


def test_add_opinion(client,auth_web, user):

    assert auth_web.status_code == 302

    response = client.post(
        "/opinions/add",
        data={
            "title": "Test opinion",
            "text": "Test text of opinion: SUPER",
            "source": "IMDb"
        },
        follow_redirects=True
    )

    assert response.status_code == 200

    from opinions_app.models import Opinion, OpinionStatus

    new_opinion = Opinion.query.first()

    assert new_opinion
    assert new_opinion.status == OpinionStatus.PENDING

def test_update_opinion(client, auth_web, user, opinion):

    assert auth_web.status_code == 302

    response = client.post(
        f"/opinions/{opinion.id}/redact",
        data = {
            "title": "Updated Opinion",
            "text": "Updated Text Opinion"
        },
        follow_redirects = True
    )

    assert response.status_code == 200

    from opinions_app.models import Opinion, OpinionStatus

    updated_opinion = Opinion.query.get(opinion.id)

    assert updated_opinion.status == OpinionStatus.PENDING





