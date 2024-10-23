import uuid
from enum import Enum


class FilmEmulsionType(Enum):
    UNDEFINED = 0
    BLACK_WHITE_PAN = 1
    BLACK_WHITE_ORTHO = 2
    COLOR = 3
    INFRARED = 4


class FilmFormat(Enum):
    UNDEFINED = 0
    THIRTY_FIVE_MM = 1
    ONE_TWENTY = 2
    ONE_TWENTY_SEVEN = 3
    ONE_TEN = 4
    SHEET_4x5in = 5
    SHEET_6x7in = 6
    SHEET_8x10in = 7
    SHEET_12x20in = 8
    SHEET_GENERIC = 9


class FilmStockVariant:
    def __init__(self,
                 iso: int,
                 format: FilmFormat | int,
                 uid: str | uuid.UUID | None = None):
        if uid is None:
            self.uid = uuid.uuid4().__str__()
        else:
            self.uid = uid.__str__() if type(uid) is uuid.UUID else uuid.UUID(uid).__str__()
        self.iso = iso
        self.format = format if type(format) is FilmFormat else FilmFormat(format)

    @classmethod
    def from_db(cls, row):
        return cls(uid=row[0],
                   iso=row[2],
                   format=FilmFormat(row[3]))

    def to_dict(self):
        return {
            "iso": self.iso,
            "format": self.format.value,
            "format_name": self.format.__str__(),
        }


class FilmStock:
    def __init__(self,
                 name: str,
                 emulsion_type: FilmEmulsionType | int,
                 variants: list[FilmStockVariant] = [],
                 uid: str | uuid.UUID | None = None,
                 info: str | None = None):
        if uid is None:
            self.uid = uuid.uuid4().__str__()
        else:
            self.uid = uid.__str__() if type(uid) is uuid.UUID else uuid.UUID(uid).__str__()
        self.name: str = name
        self.emulsion_type: FilmEmulsionType = emulsion_type if type(emulsion_type) is FilmEmulsionType else FilmEmulsionType(emulsion_type)
        self.variants: list[FilmStockVariant] = variants
        self.info: str = info

    @classmethod
    def from_db(cls,
                row,
                variants: list[FilmStockVariant]):
        return cls(uid=row[0],
                   name=row[1],
                   info=row[2],
                   emulsion_type=FilmEmulsionType(row[3]),
                   variants=variants)

    def to_dict(self) -> dict:
        return {
            "uid": self.uid,
            "name": self.name,
            "emulsion_type": self.emulsion_type.value,
            "emulsion_type_name": self.emulsion_type.__str__(),
            "info": self.info,
            "variants": [variant.to_dict() for variant in self.variants],
        }

