import pytest
from pydantic import ValidationError

from api.dtos.translate_result_dto import TranslateResultDTO


@pytest.fixture
def valid_data() -> dict[str, str]:
    return {
        "content": "translation result",
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
    assert dto.content == valid_data["content"]


def test_translate_result_dto_invalid(invalid_data: dict[str, str]) -> None:
    # When / Then
    with pytest.raises(ValidationError):
        TranslateResultDTO(**invalid_data)


def test_translate_result_dto_empty_content() -> None:
    # Given
    data = {
        "content": "",
    }

    # When
    dto = TranslateResultDTO(**data)

    # Then
    assert dto.content == data["content"]
