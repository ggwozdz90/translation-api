import pytest
from pydantic import ValidationError

from api.dtos.translate_result_dto import TranslateResultDTO


@pytest.fixture
def valid_data() -> dict[str, str]:
    return {
        "translation": "translation result",
    }


@pytest.fixture
def invalid_data() -> dict[str, str]:
    return {
        # Missing 'content' field
    }


def test_translate_result_dto_valid(valid_data: dict[str, str]) -> None:
    # When
    dto = TranslateResultDTO(**valid_data)

    # Then
    assert dto.translation == valid_data["translation"]


def test_translate_result_dto_invalid(invalid_data: dict[str, str]) -> None:
    # When / Then
    with pytest.raises(ValidationError):
        TranslateResultDTO(**invalid_data)


def test_translate_result_dto_empty_content() -> None:
    # Given
    data = {
        "translation": "",
    }

    # When
    dto = TranslateResultDTO(**data)

    # Then
    assert dto.translation == data["translation"]
