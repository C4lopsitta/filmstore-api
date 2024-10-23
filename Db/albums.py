import Db
from Entities.Album import Album


def create(album: Album):
    if _db_load_album(uid=album.uid) is not None:
        raise KeyError(f"Album {album.uid} already exists")

    Db.cursor.execute(f"""
        INSERT INTO albums VALUES('{album.uid}',
                                  '{album.name}',
                                  '{album.description}',
                                  '{album.owner.uid if type(album.owner) is not str else album.owner}',
                                  {album.is_shared});
    """)

    Db.connection.commit()


def fetch(uid: str) -> Album | None:
    row = _db_load_album(uid=uid)

    if row is None:
        return None

    return Album.from_db(row)


def fetch_all() -> list[Album] | None:
    items: list[Album] = []

    rows = Db.cursor.execute("SELECT * FROM albums;").fetchall()

    if len(rows) == 0 or rows[0] is None:
        return None

    for row in rows:
        items.append(Album.from_db(row))

    return items


def update(album: Album):
    if _db_load_album(uid=album.uid) is None:
        raise KeyError(f"Album {album.uid} does not exist")

    Db.cursor.execute(f"""
        UPDATE albums WHERE uid='{album.uid}' SET ;
    """)

    Db.connection.commit()


def delete(uid: str):
    if _db_load_album(uid) is None:
        raise KeyError(f"Album {uid} does not exist")

    Db.cursor.execute(f"""
        DELETE FROM albums WHERE uid='{uid}';
    """)

    Db.connection.commit()


def _db_load_album(uid: str) -> tuple:
    return Db.cursor.execute(f"SELECT * FROM albums WHERE uid = '{uid}'").fetchone()
