import sqlite3
import subprocess

from Entities.Film import Film, FilmType, FilmFormat
from Entities.FilmRoll import FilmRoll, DevelopmentStatus
from Entities.Picture import Picture

connection = sqlite3.connect('./filmstore.sqlite')

cursor = connection.cursor()

# region: init
cursor.execute("PRAGMA foreign_keys = ON;")
cursor.execute("""
CREATE TABLE if not exists films(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    iso INTEGER NOT NULL,
    info TEXT,
    type INTEGER NOT NULL
);""")
cursor.execute("""
CREATE TABLE if not exists pictures(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT,
    location TEXT,
    aperture TEXT,
    shutter TEXT,
    posted INTEGER,
    printed INTEGER,
    thumbnail TEXT NOT NULL
);""")
cursor.execute("""
CREATE TABLE if not exists filmrolls(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    film INTEGER,
    archival TEXT,
    status INTEGER NOT NULL,
    camera TEXT,
    FOREIGN KEY (film) REFERENCES films(id)
);""")
cursor.execute("""
CREATE TABLE if not exists pic_film_rel(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filmroll INTEGER,
    picture INTEGER,
    FOREIGN KEY (filmroll) REFERENCES filmrolls(id),
    FOREIGN KEY (picture) REFERENCES pictures(id)
);""")
try:
    cursor.execute("ALTER TABLE films ADD COLUMN format INTEGER NOT NULL DEFAULT 0;")
except sqlite3.OperationalError:
    pass

connection.commit()


def seed():
    rs = cursor.execute("SELECT * FROM films;").fetchall()
    if len(rs) == 0:
        default_rolls = [
            Film(name="Ilford HP5+", iso=400, development_info="", type=FilmType.BLACK_WHITE_PAN, format=FilmFormat.THIRTY_FIVE_MM),
            Film(name="Ilford FP4+", iso=125, development_info="", type=FilmType.BLACK_WHITE_PAN, format=FilmFormat.THIRTY_FIVE_MM),
            Film(name="Kodak Gold", iso=200, development_info="", type=FilmType.COLOR, format=FilmFormat.THIRTY_FIVE_MM),
            Film(name="Kodak Ultramax", iso=400, development_info="", type=FilmType.COLOR, format=FilmFormat.THIRTY_FIVE_MM),
            Film(name="Ilford SFX", iso=200, development_info="", type=FilmType.INFRARED, format=FilmFormat.THIRTY_FIVE_MM),
            Film(name="Harman Phoenix", iso=200, development_info="", type=FilmType.COLOR, format=FilmFormat.THIRTY_FIVE_MM),
            Film(name="Fomapan 100", iso=100, development_info="", type=FilmType.BLACK_WHITE_PAN, format=FilmFormat.ONE_TWENTY)
        ]
        for film in default_rolls:
            add_film(film)
        connection.commit()


seed()
# endregion: init

def add_film(film: Film) -> int:
    cursor.execute(
        f"INSERT INTO films VALUES(NULL, '{film.name}', {film.iso}, '{film.development_info}', {film.type.value}, {film.format.value});"
    )
    connection.commit()
    cursor.execute("SELECT last_insert_rowid() FROM films;")
    return cursor.fetchone()[0]


def fetch_film(film_id: int) -> Film:
    cursor.execute("SELECT * FROM films WHERE id=?;", (film_id,))

    row = cursor.fetchone()

    return Film(db_id=row[0],
                name=row[1],
                iso=row[2],
                development_info=row[3],
                type=FilmType(row[4]),
                format=FilmFormat(row[5]))


def fetch_films(filter_type: FilmType = None) -> list[Film]:
    if filter_type is None:
        rows = cursor.execute('SELECT * FROM films;')
    else:
        rows = cursor.execute(f'SELECT * FROM films WHERE {filter_type.value} = type;')

    films: list[Film] = []

    for row in rows:
        print(row)
        films.append(Film(db_id=row[0],
                          name=row[1],
                          iso=row[2],
                          format=FilmFormat(row[5]),
                          development_info=row[3],
                          type=FilmType(row[4])))

    return films


def add_picture(picture: Picture) -> int:
    cursor.execute(
        f"INSERT INTO pictures VALUES(NULL, '{picture.description}', '{picture.location}',"
        f" {picture.aperture}, '{picture.shutter_speed}', {1 if picture.posted else 0}, {1 if picture.printed else 0},"
        f"'{picture.thumbnail}');"
    )
    connection.commit()
    cursor.execute(f"SELECT last_insert_rowid() as ID FROM pictures;")
    return cursor.fetchone()[0]


def fetch_picture(picture_id: int) -> Picture:
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


def add_filmroll(filmroll: FilmRoll) -> int:
    cursor.execute("INSERT INTO filmrolls VALUES(NULL, ?, ?, ?, ?)",
                   (filmroll.film.db_id, filmroll.archival_identifier, filmroll.status.value, filmroll.camera))
    connection.commit()

    cursor.execute("SELECT last_insert_rowid() as ID FROM filmrolls;")
    filmroll_id = cursor.fetchone()[0]

    for picture in filmroll.pictures:
        cursor.execute(f"INSERT INTO pic_film_rel VALUES(NULL, ?, ?)", (filmroll_id, picture.db_id))

    connection.commit()

    return filmroll_id

def fetch_filmroll(filmroll_id: int) -> FilmRoll:
    rows = cursor.execute(
        f"SELECT pictures.* FROM pictures, pic_film_rel WHERE pic_film_rel.filmroll = {filmroll_id} AND pic_film_rel.picture = pictures.id;"
    )

    pictures: list[Picture] = []

    for row in rows:
        pictures.append(Picture(db_id=row[0],
                                description=row[1],
                                location=row[2],
                                aperture=row[3],
                                shutter_speed=row[4],
                                posted= True if row[5] == 1 else False,
                                printed=True if row[6] == 1 else False,
                                thumbnail=row[7]))

    cursor.execute(f"SELECT * FROM filmrolls WHERE id={filmroll_id};")

    row = cursor.fetchone()

    film_id = row[1]

    return FilmRoll(db_id=row[0],
                    film=fetch_film(film_id),
                    archival_identifier=row[2],
                    status=row[3],
                    pictures=pictures,
                    camera=row[4])


def fetch_filmrolls() -> list[FilmRoll]:
    rows = cursor.execute('SELECT * FROM filmrolls;')

    filmrolls: list[FilmRoll] = []

    rolls_rows = []

    for row in rows:
        rolls_rows.append(row)

    for row in rolls_rows:
        print(row)
        pictures: list[Picture] = []
        picrows = cursor.execute(
            f"SELECT pictures.* FROM pictures, pic_film_rel WHERE pic_film_rel.filmroll = {row[0]} AND pic_film_rel.picture = pictures.id;"
        )
        for picrow in picrows:
            pictures.append(Picture(db_id=picrow[0],
                                    description=picrow[1],
                                    location=picrow[2],
                                    aperture=picrow[3],
                                    shutter_speed=picrow[4],
                                    posted=True if picrow[5] == 1 else False,
                                    printed=True if picrow[6] == 1 else False,
                                    thumbnail=picrow[7]))
        filmrolls.append(FilmRoll(db_id=row[0],
                                  film=fetch_film(row[1]),
                                  archival_identifier=row[2],
                                  pictures=pictures,
                                  status=DevelopmentStatus(row[3]),
                                  camera=row[4]))

    return filmrolls


def delete_film_stock(film_stock_id: int) -> (list[str], int):
    rows = cursor.execute(f"SELECT * FROM filmrolls WHERE film = {film_stock_id};")
    films: list[int] = []

    files_to_delete: list[str] = []

    for row in rows:
        films.append(row[0])

    for film in films:
        rows = cursor.execute(f"SELECT pictures.* FROM pictures, pic_film_rel WHERE pic_film_rel.filmroll = {film};")
        for row in rows:
            files_to_delete.append(row[7])
        cursor.execute(f"DELETE FROM pictures pic_film_rel WHERE pic_film_rel.filmroll = {film} AND pic_film_rel.picture = pictures.id;")
        cursor.execute(f"DELETE FROM filmrolls WHERE film = {film_stock_id};")

    cursor.execute(f"DELETE FROM films WHERE id={film_stock_id};")
    connection.commit()

    return files_to_delete, len(films)


