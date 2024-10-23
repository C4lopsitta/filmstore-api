import uuid

from Entities.User import User


class Album():
    def __init__(self,
                 name: str,
                 is_shared: bool = False,
                 owner: User | None = None,
                 description: str | None = None,
                 uid: str | uuid.UUID | None = None):
        if uid is None:
            self.uid = uuid.uuid4().__str__()
        else:
            self.uid = uid.__str__() if type(uid) is uuid.UUID else uuid.UUID(uid).__str__()

        self.name = name
        self.is_shared = is_shared
        self.owner = owner
        self.description = description

    def to_dict(self) -> dict:
        return {
            "uid": self.uid,
            "name": self.name,
            "is_shared": self.is_shared,
            "owner": self.owner,
            "description": self.description
        }