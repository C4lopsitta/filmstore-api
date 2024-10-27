import uuid
from enum import Enum

import Entities

class _ImageMime():
    def __init__(self,
                 mime: str,
                 is_raw: bool,
                 extension: str):
        self.mime = mime
        self.is_raw = is_raw
        self.extension = extension


class ImageMimeType(Enum):
    """
    Enumeration of supported image mime types. Values are tuples composed by the str mime type and a bool. When True the
    format is to be considered RAW, when False the format is to be considered compressed.
    """
    UNDEFINED = _ImageMime("", False, "")
    JPEG = _ImageMime("image/jpeg", False, "jpeg")
    PNG = _ImageMime("image/png", False, "png")
    HEIC = _ImageMime("image/heic", False, "heic")
    TIFF = _ImageMime("image/tiff", True, "tiff")
    NEF = _ImageMime("image/x-nikon-nef", True, "nef")
    DNG = _ImageMime("image/x-adobe-dng", True, "dng")
    CR3 = _ImageMime("image/x-canon-cr3", True, "cr3")
    CR2 = _ImageMime("image/x-canon-cr2", True, "cr2")
    CRW = _ImageMime("image/x-canon-crw", True, "crw")

    @classmethod
    def from_str(cls, mime_type: str):
        for mime in ImageMimeType.__members__.values():
            if mime.value.mime == mime_type:
                return mime
        raise Exception("Unsupported image mime type.")



class Picture:
    def __init__(self,
                 filename: str,
                 image_mime_type: ImageMimeType | str,
                 title: str | None = None,
                 description: str | None = None,
                 location: str | None = None,
                 is_location_coordinates: bool = False,
                 aperture: str | None = None,
                 shutter_speed: str | None = None,
                 flickr_post_url: str | None = None,
                 owner: Entities.User | str | None = None,
                 film_roll: Entities.FilmRoll | str | None = None,
                 album: Entities.Album | str | None = None,
                 project: Entities.Project | str | None = None,
                 uid: str | uuid.UUID | None = None):
        if uid is None:
            self.uid = uuid.uuid4().__str__()
        else:
            self.uid = uid.__str__() if type(uid) is uuid.UUID else uuid.UUID(uid).__str__()

        self.filename = filename
        self.image_mime_type = image_mime_type if type(image_mime_type) is ImageMimeType else ImageMimeType(image_mime_type)
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
                   project=row[12],
                   image_mime_type=row[13])

    def to_dict(self) -> dict:
        return {
            "uid": self.uid,
            "filename": self.filename,
            "title": self.title,
            "description": self.description,
            "image_mime_type": self.image_mime_type.value,
            "location": self.location,
            "is_location_coordinates": self.is_location_coordinates,
            "aperture": self.aperture,
            "shutter_speed": self.shutter_speed,
            "flickr_post_url": self.flickr_post_url,
            "owner_uid": self.owner.uid if type(self.owner) is Entities.User else self.owner,
            "film_roll_uid": self.film_roll.uid if type(self.film_roll) is Entities.FilmRoll else self.film_roll,
            "album_uid": self.album.uid if type(self.album) is Entities.Album else self.album,
            "project_uid": self.project.uid if type(self.project) is Entities.Project else self.project,
        }
