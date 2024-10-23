import uuid

from Entities.Album import Album
from Entities.FilmRoll import FilmRoll
from Entities.Project import Project
from Entities.User import User


class Picture:
    def __init__(self,
                 filename: str,
                 title: str | None = None,
                 description: str | None = None,
                 location: str | None = None,
                 is_location_coordinates: bool = False,
                 aperture: str | None = None,
                 shutter_speed: str | None = None,
                 flickr_post_url: str | None = None,
                 owner: User | str | None = None,
                 film_roll: FilmRoll | str | None = None,
                 album: Album | str | None = None,
                 project: Project | str | None = None,
                 uid: str | uuid.UUID | None = None):
        if uid is None:
            self.uid = uuid.uuid4().__str__()
        else:
            self.uid = uid.__str__() if type(uid) is uuid.UUID else uuid.UUID(uid).__str__()

        self.filename = filename
        self.title = title
        self.description = description
        self.location = location
        self.is_location_coordinates = is_location_coordinates
        self.aperture = aperture
        self.shutter_speed = shutter_speed
        self.flickr_post_url = flickr_post_url
        self.owner = owner
        self.film_roll = film_roll
        self.album = album
        self.project = project

    @classmethod
    def from_db(cls, row: tuple):
        return cls(uid=row[0],
                   title=row[1],
                   description=row[2],
                   location=row[3],
                   is_location_coordinates=row[4],
                   aperture=row[5],
                   shutter_speed=row[6],
                   flickr_post_url=row[7],
                   filename=row[8],
                   owner=row[9],
                   film_roll=row[10],
                   album=row[11],
                   project=row[12])

    def to_dict(self) -> dict:
        return {
            "uid": self.uid,
            "filename": self.filename,
            "title": self.title,
            "description": self.description,
            "location": self.location,
            "is_location_coordinates": self.is_location_coordinates,
            "aperture": self.aperture,
            "shutter_speed": self.shutter_speed,
            "flickr_post_url": self.flickr_post_url,
            "owner_uid": self.owner.uid if type(self.owner) is User else self.owner,
            "film_roll_uid": self.film_roll.uid if type(self.film_roll) is FilmRoll else self.film_roll,
            "album_uid": self.album.uid if type(self.album) is Album else self.album,
            "project_uid": self.project.uid if type(self.project) is Project else self.project,
        }
