from abc import ABC, abstractmethod
from typing import Any, Dict


class TranslationModelRepository(ABC):
    @abstractmethod
    def translate(
        self,
        text_to_translate: str,
        source_language: str,
        target_language: str,
        generation_parameters: Dict[str, Any],
    ) -> str:
        pass
