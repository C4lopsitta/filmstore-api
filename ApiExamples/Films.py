from typing import Annotated

from fastapi import Body
from pydantic import BaseModel


class Films(BaseModel):
    name: str
    iso: int
    development_info: str | None = None
    type: int
    format: int


FilmsExample: Annotated[
    Films,
    Body(
        example={
            "name": "Lomography Berlin Kino",
            "iso": 400,
            "development_info": "",
            "type": 1,
            "format": 1
        }
    )
]
