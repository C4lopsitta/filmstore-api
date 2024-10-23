from enum import Enum
from Entities.Picture import Picture
from Entities.FilmStock import FilmStock


class DevelopmentStatus(Enum):
    UNDEFINED = 0
    IN_CAMERA = 1
    TO_DEVELOP = 2
    DEVELOPED = 3
    SCANNED = 4
    ARCHIVED = 5


class FilmRoll:
    def __init__(self,
                 camera: str,
                 film: FilmStock,
                 archival_identifier: str,
                 pictures: list[Picture],
                 db_id: int = None,
                 status: DevelopmentStatus = DevelopmentStatus.UNDEFINED):
        self.db_id = db_id
        self.camera = camera
        self.film = film
        self.archival_identifier = archival_identifier
        self.pictures = pictures
        self.status = status

    def to_tuple(self) -> tuple:
        return self.db_id, self.camera, self.film, self.archival_identifier, self.pictures, self.status.value

    def to_dict(self) -> dict:
        return {
            "camera": self.camera,
            "film": self.film.to_dict(),
            "status": self.status.value,
            "db_id": self.db_id,
            "pictures": [picture.db_id for picture in self.pictures],
            "identifier": self.archival_identifier,
        }
