import Db
from Entities.FilmRoll import FilmRoll, DevelopmentStatus
from Entities.Picture import Picture


def create(film_roll: FilmRoll):
    pass

def _create(filmroll: FilmRoll) -> int:
    Db.cursor.execute("INSERT INTO filmrolls VALUES(NULL, ?, ?, ?, ?)",
                      (filmroll.film.db_id, filmroll.archival_identifier, filmroll.status.value, filmroll.camera))
    Db.connection.commit()

    Db.cursor.execute("SELECT last_insert_rowid() as ID FROM filmrolls;")
    filmroll_id = Db.cursor.fetchone()[0]

    for picture in filmroll.pictures:
        Db.cursor.execute(f"INSERT INTO pic_film_rel VALUES(NULL, ?, ?)", (filmroll_id, picture.db_id))

    Db.connection.commit()

    return filmroll_id


def _fetch(filmroll_id: int) -> FilmRoll:
    rows = Db.cursor.execute(
        f"SELECT pictures.* FROM pictures, pic_film_rel WHERE pic_film_rel.filmroll = {filmroll_id} AND pic_film_rel.picture = pictures.id;"
    )

    pictures: list[Picture] = []

    for row in rows:
        pictures.append(Picture(db_id=row[0],
                                description=row[1],
                                location=row[2],
                                aperture=row[3],
                                shutter_speed=row[4],
                                posted=True if row[5] == 1 else False,
                                printed=True if row[6] == 1 else False,
                                thumbnail=row[7]))

    Db.cursor.execute(f"SELECT * FROM filmrolls WHERE id={filmroll_id};")

    row = Db.cursor.fetchone()

    film_id = row[1]

    return FilmRoll(db_id=row[0],
                    film=Db.film_stocks.fetch(film_id),
                    archival_identifier=row[2],
                    status=row[3],
                    pictures=pictures,
                    camera=row[4])


def _fetch_all(stock_filter: int) -> list[FilmRoll]:
    if stock_filter == 0:
        rows = Db.cursor.execute('SELECT * FROM filmrolls;')
    else:
        rows = Db.cursor.execute(f"SELECT * FROM filmrolls WHERE film = {stock_filter};")

    filmrolls: list[FilmRoll] = []

    rolls_rows = []

    for row in rows:
        rolls_rows.append(row)

    for row in rolls_rows:
        print(row)
        pictures: list[Picture] = []
        if stock_filter == 0:
            picrows = Db.cursor.execute(
                f"SELECT pictures.* FROM pictures, pic_film_rel WHERE "
                f"pic_film_rel.filmroll = {row[0]} "
                f"AND pic_film_rel.picture = pictures.id;"
            )
        else:
            picrows = Db.cursor.execute(
                f"SELECT pictures.* FROM pictures, pic_film_rel, filmrolls WHERE "
                f"pic_film_rel.filmroll = {row[0]} "
                f"AND pic_film_rel.picture = pictures.id AND "
                f"filmrolls.film = {stock_filter};"
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
                                  film=Db.film_stocks.fetch(row[1]),
                                  archival_identifier=row[2],
                                  pictures=pictures,
                                  status=DevelopmentStatus(row[3]),
                                  camera=row[4]))

    return filmrolls
