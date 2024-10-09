from Entities.Picture import Picture
from db import cursor, connection


def create(picture: Picture) -> int:
    cursor.execute(
        f"INSERT INTO pictures VALUES(NULL, '{picture.description}', '{picture.location}',"
        f" {picture.aperture}, '{picture.shutter_speed}', {1 if picture.posted else 0}, {1 if picture.printed else 0},"
        f"'{picture.thumbnail}');"
    )
    connection.commit()
    cursor.execute(f"SELECT last_insert_rowid() as ID FROM pictures;")
    return cursor.fetchone()[0]


def fetch_all() -> list[Picture]:
    rs = cursor.execute('SELECT * FROM pictures;')

    pictures: list[Picture] = []
    for row in rs:
        pictures.append(Picture(db_id=row[0],
                                description=row[1],
                                location=row[2],
                                aperture=row[3],
                                shutter_speed=row[4],
                                posted=True if row[5] > 0 else False,
                                printed=True if row[6] > 0 else False,
                                thumbnail=row[7]))

    return pictures


def fetch(picture_id: int) -> Picture:
    cursor.execute(f"SELECT * FROM pictures WHERE id=?;", (picture_id,))
    picture = cursor.fetchone()
    return Picture(db_id=picture[0],
                   description=picture[1],
                   location=picture[2],
                   aperture=picture[3],
                   shutter_speed=picture[4],
                   posted=True if picture[5] > 0 else False,
                   printed=True if picture[6] > 0 else False,
                   thumbnail=picture[7])


