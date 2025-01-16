import pytest
from pydantic import ValidationError

from src.api.dtos.translate_dto import TranslateDTO


def test_translate_dto_valid_languages() -> None:
    # Given
    valid_source_language = "en_US"
    valid_target_language = "es_ES"

    # When
    dto = TranslateDTO(
        text_to_translate="Hello, how are you?",
        source_language=valid_source_language,
        target_language=valid_target_language,
    )

    # Then
    assert dto.source_language == valid_source_language
    assert dto.target_language == valid_target_language
    assert dto.text_to_translate == "Hello, how are you?"


def test_translate_dto_invalid_source_language() -> None:
    # Given
    invalid_source_language = "english_US"

    # When / Then
    with pytest.raises(ValidationError) as exc_info:
        TranslateDTO(
            text_to_translate="Hello, how are you?",
            source_language=invalid_source_language,
            target_language="es_ES",
        )

    assert "Invalid language format. Expected format is xx_XX" in str(exc_info.value)


def test_translate_dto_invalid_target_language() -> None:
    # Given
    invalid_target_language = "spanish_ES"

    # When / Then
    with pytest.raises(ValidationError) as exc_info:
        TranslateDTO(
            text_to_translate="Hello, how are you?",
            source_language="en_US",
            target_language=invalid_target_language,
        )

    assert "Invalid language format. Expected format is xx_XX" in str(exc_info.value)
