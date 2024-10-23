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
                 stock: FilmStock | str,
                 is_shared: bool = False,
                 pictures: list[Picture] | None = None,
                 camera: Camera | str | None = None,
                 project: Project | str | None = None,
                 album: Album | str | None = None,
                 owner: User | str | None = None,
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
        self.is_shared = is_shared

    @classmethod
    def from_db(cls,
                row: tuple):
        return cls(uid=row[0],
                   archival_id=row[1],
                   date_start_shooting=row[2],
                   date_end_shooting=row[3],
                   stock=row[4],
                   camera=row[5],
                   project=row[6],
                   album=row[7],
                   owner=row[8],
                   is_shared=row[9])

    def to_dict(self) -> dict:
        return {
            "uid": self.uid,
            "archival_id": self.archival_id,
            "stock_uid": self.stock.uid if type(self.stock.uid) is not str else self.stock,
            "camera_uid": self.camera.uid if type(self.camera.uid) is not str else self.camera,
            "project_uid": self.project.uid if type(self.project.uid) is not str else self.project,
            "album_uid": self.album.uid if type(self.album.uid) is not str else self.album,
            "owner_uid": self.owner.uid if type(self.owner.uid) is not str else self.owner,
            "date_start_shooting": self.date_start_shooting,
            "date_end_shooting": self.date_end_shooting,
            "is_shared": self.is_shared,
        }

