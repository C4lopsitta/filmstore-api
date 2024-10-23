import uuid

import Entities


class Album():
    def __init__(self,
                 name: str,
                 is_shared: bool = False,
                 owner: Entities.User | str | None = None,
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

    @classmethod
    def from_db(cls, row: tuple):
        return cls(uid=row[0],
                   name=row[1],
                   description=row[2],
                   owner=row[3],
                   is_shared=row[4],)

    def to_dict(self) -> dict:
        return {
            "uid": self.uid,
            "name": self.name,
            "is_shared": self.is_shared,
            "owner_uid": self.owner.uid if type(self.owner) is Entities.User else self.owner,
            "description": self.description
        }
