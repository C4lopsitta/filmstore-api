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
        # TODO)) Password

    def to_dict(self) -> dict:
        return {
            "uid": self.uid,
            "username": self.username
        }

