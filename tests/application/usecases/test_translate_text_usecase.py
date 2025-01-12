from unittest.mock import Mock

import pytest

from application.usecases.translate_text_usecase import TranslateTextUseCase
from core.config.app_config import AppConfig
from core.logger.logger import Logger
from domain.services.translation_service import TranslationService


@pytest.fixture
def mock_logger() -> Logger:
    return Mock(Logger)


@pytest.fixture
def mock_config() -> AppConfig:
    return Mock(AppConfig)


@pytest.fixture
def mock_translation_service() -> TranslationService:
    return Mock(TranslationService)


@pytest.fixture
def use_case(
    mock_config: AppConfig,
    mock_logger: Logger,
    mock_translation_service: TranslationService,
) -> TranslateTextUseCase:
    return TranslateTextUseCase(
        config=mock_config,
        logger=mock_logger,
        translation_service=mock_translation_service,
    )


@pytest.mark.asyncio
async def test_execute_success(
    use_case: TranslateTextUseCase,
    mock_translation_service: Mock,
) -> None:
    # Given
    mock_translation_service.translate_text = Mock(return_value="translated_result")

    # When
    result = await use_case.execute("Hello", "en", "pl")

    # Then
    assert result == "translated_result"
    mock_translation_service.translate_text.assert_called_once_with("Hello", "en", "pl")
