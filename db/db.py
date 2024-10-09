from db import connection, cursor

from Entities.Film import Film, FilmType, FilmFormat
from Entities.FilmRoll import FilmRoll, DevelopmentStatus
from Entities.Picture import Picture


# endregion: init




def delete_film_stock(film_stock_id: int) -> (list[str], int):
    rows = cursor.execute(f"SELECT * FROM filmrolls WHERE film = {film_stock_id};")
    films: list[int] = []

    files_to_delete: list[str] = []

    for row in rows:
        films.append(row[-1])

    for film in films:
        rows = cursor.execute(f"SELECT pictures.* FROM pictures, pic_film_rel WHERE pic_film_rel.filmroll = {film};")
        for row in rows:
            files_to_delete.append(row[6])
        cursor.execute(f"DELETE FROM pictures pic_film_rel WHERE pic_film_rel.filmroll = {film} AND pic_film_rel.picture = pictures.id;")
        cursor.execute(f"DELETE FROM filmrolls WHERE film = {film_stock_id};")

    cursor.execute(f"DELETE FROM films WHERE id={film_stock_id};")
    connection.commit()

    return files_to_delete, len(films)

