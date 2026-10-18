from pydantic import BaseModel
from typing import Optional


class VagaResponse(BaseModel):
    hash_vaga: str
    titulo: str
    empresa: str
    fonte: str
    local: Optional[str] = None
    remoto: bool
    url: str


    class Config:
        from_attributes = True


