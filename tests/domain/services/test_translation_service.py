from unittest.mock import Mock

import pytest

from core.config.app_config import AppConfig
from core.logger.logger import Logger
from domain.repositories.translation_model_repository import TranslationModelRepository
from domain.services.language_mapping_service import LanguageMappingService
from domain.services.translation_service import TranslationService


@pytest.fixture
def mock_logger() -> Logger:
    return Mock(Logger)


@pytest.fixture
def mock_config() -> AppConfig:
    config = Mock(AppConfig)
    config.translation_model_name = "test_model"
    return config


@pytest.fixture
def mock_translation_model_repository() -> TranslationModelRepository:
    return Mock(TranslationModelRepository)


@pytest.fixture
def mock_language_mapping_service() -> LanguageMappingService:
    return Mock(LanguageMappingService)


@pytest.fixture
def translation_service(
    mock_logger: Logger,
    mock_config: AppConfig,
    mock_translation_model_repository: TranslationModelRepository,
    mock_language_mapping_service: LanguageMappingService,
) -> TranslationService:
    return TranslationService(
        logger=mock_logger,
        config=mock_config,
        translation_model_repository=mock_translation_model_repository,
        language_mapping_service=mock_language_mapping_service,
    )


def test_translate_text_success(
    translation_service: TranslationService,
    mock_translation_model_repository: TranslationModelRepository,
    mock_language_mapping_service: LanguageMappingService,
) -> None:
    # Given
    text = "Hello World"
    source_language = "en"
    target_language = "es"
    mock_language_mapping_service.map_language.side_effect = ["en", "es"]
    mock_translation_model_repository.translate.return_value = "Hola Mundo"

    # When
    result = translation_service.translate_text(text, source_language, target_language)

    # Then
    assert result == "Hola Mundo"
    mock_translation_model_repository.translate.assert_called_once_with(text, source_language, target_language)


def test_translate_text_exception(
    translation_service: TranslationService,
    mock_translation_model_repository: TranslationModelRepository,
    mock_language_mapping_service: LanguageMappingService,
) -> None:
    # Given
    text = "Hello World"
    source_language = "en"
    target_language = "es"
    mock_language_mapping_service.map_language.side_effect = ["en", "es"]
    mock_translation_model_repository.translate.side_effect = Exception("Translation error")

    # When / Then
    with pytest.raises(Exception, match="Translation error"):
        translation_service.translate_text(text, source_language, target_language)
