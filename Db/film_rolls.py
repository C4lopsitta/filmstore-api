import Db
from Entities.FilmRoll import FilmRoll, DevelopmentStatus
from Entities.FilmStock import FilmStockVariant


def create(film_roll: FilmRoll):
    if _db_load_roll(uid=film_roll.uid) is not None:
        raise KeyError(f"Roll {film_roll.uid} already exists")

    Db.cursor.execute(f"""
        INSERT INTO filmRolls VALUES('{film_roll.uid}',
                                     '{film_roll.archival_id}',
                                     '{film_roll.date_start_shooting}',
                                     '{film_roll.date_end_shooting}',
                                     '{film_roll.stock.uid if type(film_roll.stock) is not str else film_roll.stock}',
                                     '{film_roll.camera.uid if type(film_roll.camera) is not str else film_roll.camera}',
                                     '{film_roll.project.uid if type(film_roll.project) is not str else film_roll.project}',
                                     '{film_roll.album.uid if type(film_roll.album) is not str else film_roll.album}',
                                     '{film_roll.owner.uid if type(film_roll.owner) is not str else film_roll.owner}',
                                     {film_roll.is_shared})
    """)

    Db.connection.commit()


def fetch(uid: str) -> FilmRoll | None:
    row = _db_load_roll(uid=uid)

    if row is None:
        return None

    return FilmRoll.from_db(row=row)


def fetch_all(stock_filter: FilmStockVariant | str | None = None) -> list[FilmRoll] | None:
    rolls: list[FilmRoll] = []

    if stock_filter is None:
        rows = Db.cursor.execute("SELECT * FROM filmRolls;").fetchall()
    else:
        stock_filter = stock_filter.__str__() if type(stock_filter) is str else stock_filter
        rows = Db.cursor.execute(f"SELECT * FROM filmRolls WHERE stock = '{stock_filter}';").fetchall()

    if len(rows) == 0 or rows[0] is None:
        return None

    for row in rows:
        rolls.append(FilmRoll.from_db(row=row))

    return rolls


def update(film_roll: FilmRoll):
    if _db_load_roll(uid=film_roll.uid) is None:
        raise KeyError(f"Roll {film_roll.uid} does not exist")

    Db.cursor.execute(f"""
        UPDATE filmRolls WHERE uid='{film_roll.uid}' SET archival_id='{film_roll.archival_id}',
                                                         stock='{film_roll.stock.uid if type(film_roll.stock) is not str else film_roll.stock}',
                                                         camera='{film_roll.camera.uid if type(film_roll.camera) is not str else film_roll.camera}',
                                                         project='{film_roll.project.uid if type(film_roll.project) is not str else film_roll.project}',
                                                         album='{film_roll.album.uid if type(film_roll.album) is not str else film_roll.album}',
                                                         isShared='{film_roll.is_shared}'
                                                         startShooting='{film_roll.date_start_shooting}',
                                                         endShooting='{film_roll.date_end_shooting}';
    """)

    Db.connection.commit()


def delete(uid: str):
    if _db_load_roll(uid) is None:
        raise KeyError(f"Roll {uid} does not exist")

    Db.cursor.execute(f"""
        DELETE FROM filmRolls WHERE uid='{uid}';
    """)

    Db.connection.commit()


def _db_load_roll(uid: str) -> tuple:
    return Db.cursor.execute(f"SELECT * FROM filmRolls WHERE uid = '{uid}'").fetchone()

