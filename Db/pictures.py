import Db
from Entities.Picture import Picture


def create(picture: Picture):
    if _db_load_picture(uid=picture.uid) is not None:
        raise KeyError(f"Picture {picture.uid} already exists")

    Db.cursor.execute(f"""
        INSERT INTO pictures VALUES('{picture.uid}',
                                    '{picture.title}',
                                    '{picture.description}',
                                    '{picture.location}',
                                    {picture.is_location_coordinates},
                                    '{picture.aperture}',
                                    '{picture.shutter_speed}',
                                    '{picture.flickr_post_url}',
                                    '{picture.filename}',
                                    '{picture.owner.uid if type(picture.owner) is not str else None}',
                                    '{picture.film_roll.uid if type(picture.film_roll) is not str else None}',
                                    '{picture.album.uid if type(picture.album) is not str else None}',
                                    '{picture.project.uid if type(picture.project) is not str else None}',
                                    '{picture.image_mime_type.value if type(picture.image_mime_type) is not str else picture.image_mime_type}';
    """)

    Db.connection.commit()


def fetch(uid: str) -> Picture | None:
    row = _db_load_picture(uid=uid)

    if row is None:
        return None

    return Picture.from_db(row)


def fetch_all() -> list[Picture] | None:
    items: list[Picture] = []

    rows = Db.cursor.execute("SELECT * FROM pictures;").fetchall()

    if len(rows) == 0 or rows[0] is None:
        return None

    for row in rows:
        items.append(Picture.from_db(row))

    return items


def update(picture: Picture):
    if _db_load_picture(uid=picture.uid) is None:
        raise KeyError(f"Picture {picture.uid} does not exist")

    Db.cursor.execute(f"""
        UPDATE pictures WHERE uid='{picture.uid}' SET title = '{picture.title}',
                                                      description = '{picture.description}',
                                                      location = '{picture.location}',
                                                      isLocationCoordinates = {picture.is_location_coordinates},
                                                      aperture = '{picture.aperture}',
                                                      shutter = '{picture.shutter_speed}',
                                                      flickrPostUrl = '{picture.flickr_post_url}',
                                                      filename = '{picture.filename}',
                                                      filmRoll = '{picture.film_roll}',
                                                      album = '{picture.album}',
                                                      project = '{picture.project}';
    """)

    Db.connection.commit()


def delete(uid: str):
    if _db_load_picture(uid) is None:
        raise KeyError(f"Picture {uid} does not exist")

    Db.cursor.execute(f"""
        DELETE FROM pictures WHERE uid='{uid}';
    """)

    Db.connection.commit()


def _db_load_picture(uid: str) -> tuple:
    return Db.cursor.execute(f"SELECT * FROM pictures WHERE uid = '{uid}'").fetchone()

