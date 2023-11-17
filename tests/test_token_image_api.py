# coding: utf-8

from fastapi.testclient import TestClient


from WidgetGen.models.token_trend_data import TokenTrendData  # noqa: F401
from WidgetGen.models.token_vote_data import TokenVoteData  # noqa: F401


def test_generate_tokens_trends_image(client: TestClient):
    """Test case for generate_tokens_trends_image

    Generate an image with tokens and trends data
    """
    token_trend_data = [{"symbol":"symbol","price":0.8008282,"change":6.0274563,"name":"name","icon_url":"https://openapi-generator.tech"}]

    headers = {
    }
    response = client.request(
        "POST",
        "/generate-image/tokens-trends",
        headers=headers,
        json=token_trend_data,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_generate_tokens_votes_image(client: TestClient):
    """Test case for generate_tokens_votes_image

    Generate an image with tokens and votes data
    """
    token_vote_data = [{"symbol":"symbol","name":"name","votes":0,"icon_url":"https://openapi-generator.tech"}]

    headers = {
    }
    response = client.request(
        "POST",
        "/generate-image/tokens-votes",
        headers=headers,
        json=token_vote_data,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

