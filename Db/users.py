import Db
from Entities.User import User


def create(user: User):
    if _db_load_user(uid=user.uid, password_hash=user.password_hash) is not None:
        raise KeyError(f"User {user.uid} already exists")

    Db.cursor.execute(f"""
        INSERT INTO users VALUES('{user.uid}',
                                 '{user.username}',
                                 '{user.password_hash}');
    """)

    Db.connection.commit()


def fetch(uid: str, password_hash: str) -> User | None:
    row = _db_load_user(uid=uid, password_hash=password_hash)

    if row is None:
        return None

    return User.from_db(row)


def update(user: User):
    if _db_load_user(uid=user.uid, password_hash=user.password_hash) is None:
        raise KeyError(f"User {user.uid} does not exist")

    Db.cursor.execute(f"""
        UPDATE users WHERE uid='{user.uid}' AND passwordHash = '{user.password_hash}' SET username={user.username};
    """)

    Db.connection.commit()


def delete(uid: str, password_hash: str):
    if _db_load_user(uid, password_hash) is None:
        raise KeyError(f"User {uid} does not exist")

    Db.cursor.execute(f"""
        DELETE FROM users WHERE uid='{uid}' AND passwordHash='{password_hash}';
    """)

    Db.connection.commit()


def _db_load_user(uid: str, password_hash: str) -> tuple:
    return Db.cursor.execute(f"SELECT * FROM users WHERE uid = '{uid}' AND passwordHash='{password_hash}'").fetchone()

