import uuid

from Entities.User import User


class Project():
    def __init__(self,
                 name: str,
                 owner: User | None = None,
                 description: str | None = None,
                 location: str | None = None,
                 is_shared: bool = False,
                 is_location_coordinates: bool = False,
                 uid: str | uuid.UUID | None = None):
        if uid is None:
            self.uid = uuid.uuid4().__str__()
        else:
            self.uid = uid.__str__() if type(uid) is uuid.UUID else uuid.UUID(uid).__str__()
        self.name = name
        self.owner = owner
        self.description = description
        self.location = location
        self.is_shared = is_shared
        self.is_location_coordinates = is_location_coordinates

    def to_dict(self) -> dict:
        return {
            "uid": self.uid,
            "name": self.name,
            "owner": self.owner,
            "description": self.description,
            "location": self.location,
            "is_shared": self.is_shared,
            "is_location_coordinates": self.is_location_coordinates
        }

