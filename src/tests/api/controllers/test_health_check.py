from fastapi import status

from app.config import get_settings


class TestHealthCheck:

    settings = get_settings()

    def test_ping(self, test_app):
        response = test_app.get(f"{self.settings.prefix_api_v1}/healthcheck")
        assert response.status_code == status.HTTP_200_OK
        expected_response = {"environment": "test", "ping": "pong!"}
        assert response.json() == expected_response
