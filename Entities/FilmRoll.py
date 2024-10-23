import uuid
from enum import Enum

from Entities.Album import Album
from Entities.Camera import Camera
from Entities.Picture import Picture
from Entities.FilmStock import FilmStock
from Entities.Project import Project
from Entities.User import User


class DevelopmentStatus(Enum):
    UNDEFINED = 0
    UNUSED = 1
    IN_CAMERA = 2
    TO_DEVELOP = 3
    DEVELOPED = 4
    SCANNED = 5
    ARCHIVED = 6


class FilmRoll:
    def __init__(self,
                 archival_id: str,
                 date_start_shooting: str,
                 date_end_shooting: str,
                 stock: FilmStock,
                 pictures: list[Picture] | None = None,
                 camera: Camera | None = None,
                 project: Project | None = None,
                 album: Album | None = None,
                 owner: User | None = None,
                 uid: str | uuid.UUID | None = None):
        if uid is None:
            self.uid = uuid.uuid4().__str__()
        else:
            self.uid = uid.__str__() if type(uid) is uuid.UUID else uuid.UUID(uid).__str__()

        self.archival_id = archival_id
        self.stock = stock
        self.camera = camera
        self.project = project
        self.album = album
        self.owner = owner
        self.date_start_shooting = date_start_shooting
        self.date_end_shooting = date_end_shooting
        self.pictures = pictures

    def to_dict(self) -> dict:
        return {
            "uid": self.uid,
            "archival_id": self.archival_id,
            "stock": self.stock.uid,
            "camera": self.camera.uid,
            "project": self.project.uid,
            "album": self.album.uid,
            "owner": self.owner.uid,
            "date_start_shooting": self.date_start_shooting,
            "date_end_shooting": self.date_end_shooting,
        }

