from typing import Annotated

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
        text: str,
        source_language: str,
        target_language: str,
    ) -> str:
        self.logger.info(
            f"Executing translation for text '{text}' from '{source_language}' to '{target_language}'",
        )

        translation_result: str = self.translation_service.translate_text(
            text,
            source_language,
            target_language,
        )

        self.logger.info("Returning translation result")

        return translation_result
