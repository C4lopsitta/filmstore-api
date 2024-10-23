import uuid


class User:
    def __init__(self,
                 username: str,
                 password: str | None = None,
                 password_hash: str | None = None,
                 uid: str | uuid.UUID | None = None):
        if uid is None:
            self.uid = uuid.uuid4().__str__()
        else:
            self.uid = uid.__str__() if type(uid) is uuid.UUID else uuid.UUID(uid).__str__()

        self.username = username
        if password is None and password_hash is not None:
            self.password_hash = password_hash
        elif password is not None and password_hash is None:
            pass
        else:
            raise ValueError("Password or Password hash must be provided")

    @classmethod
    def from_db(cls, row: tuple):
        return cls(uid=row[0], username=row[1], password_hash=row[2])

    def to_dict(self) -> dict:
        return {
            "uid": self.uid,
            "username": self.username
        }

