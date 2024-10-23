import Db
from Entities.Camera import Camera


def create(camera: Camera):
    if _db_load_camera(uid=camera.uid) is not None:
        raise KeyError(f"Camera {camera.uid} already exists")

    Db.cursor.execute(f"""
        INSERT INTO cameras VALUES('{camera.uid}',
                                   '{camera.owner.uid if type(camera.owner) is not str else camera.owner}',
                                   '{camera.brand}',
                                   '{camera.model}',
                                   {camera.type.value});
    """)

    Db.connection.commit()


def fetch(uid: str) -> Camera | None:
    row = _db_load_camera(uid=uid)

    if row is None:
        return None

    return Camera.from_db(row)


def fetch_all() -> list[Camera] | None:
    items: list[Camera] = []

    rows = Db.cursor.execute("SELECT * FROM cameras;").fetchall()

    if len(rows) == 0 or rows[0] is None:
        return None

    for row in rows:
        items.append(Camera.from_db(row))

        return items


def update(camera: Camera):
    if _db_load_camera(uid=camera.uid) is None:
        raise KeyError(f"Camera {camera.uid} does not exist")

    Db.cursor.execute(f"""
        UPDATE cameras WHERE uid='{camera.uid}' SET brand = '{camera.brand}',
                                                    model = '{camera.model}',
                                                    format = {camera.type.value};
    """)

    Db.connection.commit()


def delete(uid: str):
    if _db_load_camera(uid) is None:
        raise KeyError(f"Camera {uid} does not exist")
    Db.cursor.execute(f"""
        DELETE FROM cameras WHERE uid='{uid}';
    """)

    Db.connection.commit()


def _db_load_camera(uid: str) -> tuple:
    return Db.cursor.execute(f"SELECT * FROM cameras WHERE uid = '{uid}'").fetchone()
