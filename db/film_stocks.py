from Entities.Film import Film, FilmType, FilmFormat
from db import cursor, connection


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


