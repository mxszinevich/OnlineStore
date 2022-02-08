import pytest


@pytest.fixture
def api_client() -> "APIClient":
    from rest_framework.test import APIClient

    return APIClient()
