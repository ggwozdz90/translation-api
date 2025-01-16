from pydantic import BaseModel


class TranslateResultDTO(BaseModel):
    translation: str
