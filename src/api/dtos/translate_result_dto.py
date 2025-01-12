from pydantic import BaseModel


class TranslateResultDTO(BaseModel):
    content: str
