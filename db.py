import sqlite3
from Entities.Film import Film, FilmType
from Entities.FilmRoll import FilmRoll
from Entities.Picture import Picture

connection = sqlite3.connect('./filmstore.sqlite')

cursor = connection.cursor()


def add_film(film: Film):
    cursor.execute(
        f"INSERT INTO films VALUES(NULL, '{film.name}', {film.iso}, '{film.development_info}', {film.type.value});"
    )
    connection.commit()


def fetch_film(film_id: int) -> Film:
    cursor.execute("SELECT * FROM films WHERE id=?;", (film_id,))

    row = cursor.fetchone()

    return Film(db_id=row[0],
                name=row[1],
                iso=row[2],
                development_info=row[3],
                type=FilmType(row[4]))


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



