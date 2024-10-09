import Db
from Entities.Film import Film, FilmType, FilmFormat
from Db import cursor, connection


def create(film: Film) -> int:
    cursor.execute(
        f"INSERT INTO film_stocks VALUES(NULL, '{film.name}', {film.iso}, '{film.development_info}', {film.type.value}, {film.format.value});"
    )
    connection.commit()
    cursor.execute("SELECT last_insert_rowid() FROM films;")
    return cursor.fetchone()[0]


def fetch(film_id: int) -> Film:
    cursor.execute("SELECT * FROM films WHERE id=?;", (film_id,))

    row = cursor.fetchone()

    return Film(db_id=row[0],
                name=row[1],
                iso=row[2],
                development_info=row[3],
                type=FilmType(row[4]),
                format=FilmFormat(row[5]))


def fetch_all(filter_type: FilmType = None) -> list[Film]:
    if filter_type is None:
        rows = cursor.execute('SELECT * FROM film_stocks;')
    else:
        rows = cursor.execute(f'SELECT * FROM film_stocks WHERE {filter_type.value} = type;')

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


def delete(film_stock_id: int,
           delete_rolls: bool = False,
           delete_pictures: bool = False):
    rows_rolls_to_update = cursor.execute(f"SELECT * FROM filmrolls WHERE film='{film_stock_id}';")

    for row in rows_rolls_to_update:
        if delete_rolls:
            delete_rolls_result: dict = Db.film_rolls.delete(row[0], delete_pictures)
        else:
            Db.film_rolls.update(row[0], )  # TODO))

    stock_to_delete = fetch(film_stock_id)

    cursor.execute(f"DELETE FROM film_stocks WHERE film='{film_stock_id}';")

    return {
        "rolls_affected": len(rows_rolls_to_update) if delete_rolls else 0,
        "pictures_affected": delete_rolls_result["pictures_affected"] if delete_pictures else 0,
        "stock_deleted": stock_to_delete.to_dict()
    }



















