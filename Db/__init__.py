import sqlite3

from Entities.Film import Film, FilmType, FilmFormat
from Db import film_stocks, film_rolls, pictures


connection = sqlite3.connect('./filmstore.sqlite')

cursor = connection.cursor()

# region: init
cursor.execute("PRAGMA foreign_keys = ON;")
cursor.execute("""
CREATE TABLE if not exists film_stocks(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    iso INTEGER NOT NULL,
    info TEXT,
    type INTEGER NOT NULL,
    format INTEGER NOT NULL
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
    FOREIGN KEY (film) REFERENCES film_stocks(id)
);""")
cursor.execute("""
CREATE TABLE if not exists pic_film_rel(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filmroll INTEGER,
    picture INTEGER,
    FOREIGN KEY (filmroll) REFERENCES filmrolls(id),
    FOREIGN KEY (picture) REFERENCES pictures(id)
);""")

connection.commit()


def seed():
    rs = cursor.execute("SELECT * FROM films;").fetchall()
    if len(rs) == 0:
        default_rolls = [
            Film(name="No Film",
                 iso=0,
                 development_info="",
                 type=FilmType.UNDEFINED,
                 format=FilmFormat.UNDEFINED),
            Film(name="Ilford HP5+",
                 iso=400, development_info="",
                 type=FilmType.BLACK_WHITE_PAN,
                 format=FilmFormat.THIRTY_FIVE_MM),
            Film(name="Ilford FP4+",
                 iso=125,
                 development_info="",
                 type=FilmType.BLACK_WHITE_PAN,
                 format=FilmFormat.THIRTY_FIVE_MM),
            Film(name="Kodak Gold",
                 iso=200,
                 development_info="",
                 type=FilmType.COLOR,
                 format=FilmFormat.THIRTY_FIVE_MM),
            Film(name="Kodak Ultramax",
                 iso=400, development_info="",
                 type=FilmType.COLOR,
                 format=FilmFormat.THIRTY_FIVE_MM),
            Film(name="Ilford SFX",
                 iso=200,
                 development_info="",
                 type=FilmType.INFRARED,
                 format=FilmFormat.THIRTY_FIVE_MM),
            Film(name="Harman Phoenix",
                 iso=200,
                 development_info="",
                 type=FilmType.COLOR,
                 format=FilmFormat.THIRTY_FIVE_MM),
            Film(name="Fomapan 100",
                 iso=100,
                 development_info="",
                 type=FilmType.BLACK_WHITE_PAN,
                 format=FilmFormat.ONE_TWENTY)
        ]
        for film in default_rolls:
            film_stocks.create(film)
        connection.commit()


seed()

