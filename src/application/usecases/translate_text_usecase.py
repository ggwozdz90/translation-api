from typing import Annotated, Any, Dict

from fastapi import Depends

from core.config.app_config import AppConfig
from core.logger.logger import Logger
from domain.services.translation_service import TranslationService


class TranslateTextUseCase:
    def __init__(
        self,
        config: Annotated[AppConfig, Depends()],
        logger: Annotated[Logger, Depends()],
        translation_service: Annotated[TranslationService, Depends()],
    ) -> None:
        self.config = config
        self.logger = logger
        self.translation_service = translation_service

    async def execute(
        self,
        text_to_translate: str,
        source_language: str,
        target_language: str,
        generation_parameters: Dict[str, Any],
    ) -> str:
        self.logger.info(
            f"Executing translation for text '{text_to_translate}' from '{source_language}' to '{target_language}'",
        )

        translation: str = self.translation_service.translate_text(
            text_to_translate,
            source_language,
            target_language,
            generation_parameters,
        )

        self.logger.info("Returning translation result")

        return translation
