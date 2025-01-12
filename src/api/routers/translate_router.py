from typing import Annotated

from fastapi import APIRouter, Depends

from api.dtos.translate_dto import TranslateDTO
from api.dtos.translate_result_dto import TranslateResultDTO
from application.usecases.translate_text_usecase import TranslateTextUseCase


class TranslateRouter:
    def __init__(self) -> None:
        self.router = APIRouter()
        self.router.post("/translate")(self.translate)

    async def translate(
        self,
        translate_text_usecase: Annotated[TranslateTextUseCase, Depends()],
        translate_dto: TranslateDTO = Depends(),
    ) -> TranslateResultDTO:
        result = await translate_text_usecase.execute(
            translate_dto.text,
            translate_dto.source_language,
            translate_dto.target_language,
        )

        return TranslateResultDTO(
            content=result,
        )
