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
                 owner: User | None = None,
                 film_roll: FilmRoll | None = None,
                 album: Album | None = None,
                 project: Project | None = None,
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
            "owner": self.owner.uid,
            "film_roll": self.film_roll.uid,
            "album": self.album.uid,
            "project": self.project.uid
        }
