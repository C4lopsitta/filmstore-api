from enum import Enum


class FilmType(Enum):
    UNDEFINED = 0
    BLACK_WHITE_PAN = 1
    BLACK_WHITE_ORTHO = 2
    COLOR = 3
    INFRARED = 4


class Film:
    def __init__(self, name: str,
                 iso: int,
                 type: FilmType,
                 development_info: str,
                 db_id: int = None):
        self.db_id = db_id
        self.name = name
        self.iso = iso
        self.development_info = development_info
        self.type = type

    def to_tuple(self) -> tuple:
        return self.db_id, self.name, self.iso, self.development_info, self.type.value

    def to_dict(self) -> dict:
        return {
            "id": self.db_id,
            "name": self.name,
            "iso": self.iso,
            "development_info": self.development_info,
            "type": self.type.value
        }
