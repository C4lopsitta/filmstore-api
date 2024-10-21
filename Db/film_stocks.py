import Db
from Entities.Film import Film, FilmType, FilmFormat


def create(film: Film) -> int:
    Db.cursor.execute(
        f"INSERT INTO film_stocks VALUES(NULL, '{film.name}', {film.iso}, '{film.development_info}', {film.type.value}, {film.format.value});"
    )
    Db.connection.commit()
    Db.cursor.execute("SELECT last_insert_rowid() FROM film_stocks;")
    return Db.cursor.fetchone()[0]


def fetch(film_id: int) -> Film:
    Db.cursor.execute("SELECT * FROM film_stocks WHERE id=?;", (film_id,))

    row = Db.cursor.fetchone()

    return Film(db_id=row[0],
                name=row[1],
                iso=row[2],
                development_info=row[3],
                type=FilmType(row[4]),
                format=FilmFormat(row[5]))


def fetch_all(filter_type: FilmType = None) -> list[Film]:
    if filter_type is None:
        rows = Db.cursor.execute('SELECT * FROM film_stocks;')
    else:
        rows = Db.cursor.execute(f'SELECT * FROM film_stocks WHERE {filter_type.value} = type;')

    film_stocks: list[Film] = []

    for row in rows:
        print(row)
        film_stocks.append(Film(db_id=row[0],
                          name=row[1],
                          iso=row[2],
                          format=FilmFormat(row[5]),
                          development_info=row[3],
                          type=FilmType(row[4])))

    return film_stocks


def delete(film_stock_id: int,
           delete_rolls: bool = False,
           delete_pictures: bool = False):
    rows_rolls_to_update = Db.cursor.execute(f"SELECT * FROM filmrolls WHERE film='{film_stock_id}';")

    for row in rows_rolls_to_update:
        if delete_rolls:
            delete_rolls_result: dict = Db.film_rolls.delete(row[0], delete_pictures)
        else:
            Db.film_rolls.update(row[0], )  # TODO))

    stock_to_delete = fetch(film_stock_id)

    Db.cursor.execute(f"DELETE FROM film_stocks WHERE film='{film_stock_id}';")

    return {
        "rolls_affected": len(rows_rolls_to_update) if delete_rolls else 0,
        "pictures_affected": delete_rolls_result["pictures_affected"] if delete_pictures else 0,
        "stock_deleted": stock_to_delete.to_dict()
    }



















