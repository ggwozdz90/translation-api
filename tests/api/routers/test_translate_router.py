from unittest.mock import AsyncMock, Mock

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from api.routers.translate_router import TranslateRouter
from application.usecases.translate_text_usecase import TranslateTextUseCase


@pytest.fixture
def mock_translate_text_usecase() -> TranslateTextUseCase:
    return Mock(TranslateTextUseCase)


@pytest.fixture
def client(
    mock_translate_text_usecase: TranslateTextUseCase,
) -> TestClient:
    router = TranslateRouter()
    app = FastAPI()
    app.include_router(router.router)
    app.dependency_overrides[TranslateTextUseCase] = lambda: mock_translate_text_usecase
    return TestClient(app)


def test_translate_success(
    client: TestClient,
    mock_translate_text_usecase: TranslateTextUseCase,
) -> None:
    # Given
    mock_translate_text_usecase.execute = AsyncMock(return_value="translation_result")

    # When
    response = client.post(
        "/translate",
        params={
            "text": "Hello, how are you?",
            "source_language": "en_US",
            "target_language": "pl_PL",
        },
    )

    # Then
    assert response.status_code == 200
    assert response.json() == {
        "content": "translation_result",
    }
    mock_translate_text_usecase.execute.assert_awaited_once()


def test_translate_missing_source_language(client: TestClient) -> None:
    # When
    response = client.post(
        "/translate",
    )

    # Then
    assert response.status_code == 422  # Unprocessable Entity
