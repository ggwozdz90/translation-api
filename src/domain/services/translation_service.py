from typing import Annotated

from fastapi import Depends

from core.config.app_config import AppConfig
from core.logger.logger import Logger
from data.repositories.translation_model_repository_impl import (
    TranslationModelRepositoryImpl,
)
from domain.repositories.translation_model_repository import TranslationModelRepository
from domain.services.language_mapping_service import LanguageMappingService


class TranslationService:
    def __init__(
        self,
        config: Annotated[AppConfig, Depends()],
        translation_model_repository: Annotated[TranslationModelRepository, Depends(TranslationModelRepositoryImpl)],
        logger: Annotated[Logger, Depends()],
        language_mapping_service: Annotated[LanguageMappingService, Depends()],
    ) -> None:
        self.config = config
        self.translation_model_repository = translation_model_repository
        self.logger = logger
        self.language_mapping_service = language_mapping_service

    def translate_text(
        self,
        text: str,
        source_language: str,
        target_language: str,
    ) -> str:
        self.logger.debug(f"Starting translation of text from '{source_language}' to '{target_language}'")

        source_language_mapped = self.language_mapping_service.map_language(
            source_language,
            self.config.translation_model_name,
        )
        target_language_mapped = self.language_mapping_service.map_language(
            target_language,
            self.config.translation_model_name,
        )

        translated_text: str = self.translation_model_repository.translate(
            text,
            source_language_mapped,
            target_language_mapped,
        )

        self.logger.debug("Completed translation of text")

        return translated_text
