import json
import os
import threading
from typing import Optional

from domain.exceptions.language_mapping_error import LanguageMappingError
from domain.exceptions.language_not_found_error import LanguageNotFoundError


class LanguageMappingService:
    _instance: Optional["LanguageMappingService"] = None
    _lock = threading.Lock()

    def __new__(cls) -> "LanguageMappingService":
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(LanguageMappingService, cls).__new__(cls)
                    cls._instance._initialize()

        return cls._instance

    def _initialize(self) -> None:
        self.mbart_mapping = self.load_mapping("mbart_mapping.json")
        self.seamless_mapping = self.load_mapping("seamless_mapping.json")

    def load_mapping(self, filename: str) -> dict[str, str]:
        filepath = os.path.join(os.path.dirname(__file__), "..", "..", "assets", "mappings", filename)
        with open(filepath, "r", encoding="utf-8") as file:
            return dict(sorted(json.load(file).items()))

    def map_language(self, language: str, model_type: str) -> str:
        try:
            if model_type == "facebook/mbart-large-50-many-to-many-mmt":
                return self.mbart_mapping[language]
            elif model_type == "facebook/seamless-m4t-v2-large":
                return self.seamless_mapping[language]
            else:
                raise LanguageMappingError(model_type)
        except KeyError as e:
            raise LanguageNotFoundError(language, model_type) from e
