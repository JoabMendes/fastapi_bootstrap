import logging

import pytest
from fastapi.testclient import TestClient
from testfixtures import LogCapture

from app.config import Settings, get_settings
from app.main import app

logger = logging.getLogger(__name__)


def get_settings_override() -> Settings:
    return Settings(environment="test")


@pytest.fixture(scope="module")
def test_app() -> None:
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="function", autouse=True)
def config_dependencies():
    # set default overrides for all tests
    app.dependency_overrides[get_settings] = get_settings_override
    yield
    # clean all overrides after test execution
    app.dependency_overrides = {}


@pytest.fixture()
def log_capture():
    with LogCapture() as capture:
        yield capture
