import sqlite3

from Config.config import Config
from Entities import Film
from Db import film_stocks, film_rolls, pictures

config = Config(open(file="Config/config.json", mode="r"))
connection = sqlite3.connect(config.database_file_name)

cursor = connection.cursor()

# region init
cursor.execute("PRAGMA foreign_keys=ON;")

# table users
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    VARCHAR(32) uid PRIMARY KEY,
    VARCHAR(32) username UNIQUE NOT NULL,
    TEXT passswordHash NOT NULL
);
""")

# table cameras
cursor.execute("""
CREATE TABLE IF NOT EXISTS cameras(
    VARCHAR(32) uid PRIMARY KEY,
    VARCHAR(32) owner NOT NULL,
    TEXT brand NOT NULL,
    TEXT model,
    INTEGER format,    
    FOREIGN KEY (owner) REFERENCES users(uid)
)
""")

# table filmStocks
cursor.execute("""
CREATE TABLE IF NOT EXISTS filmStocks(
    VARCHAR(32) uid PRIMARY KEY,
    TEXT name NOT NULL,
    TEXT info,
    INTEGER emulsionType NOT NULL
);
""")

# table filmStockVariant
cursor.execute("""
CREATE TABLE IF NOT EXISTS filmStockVariants(
    VARCHAR(32) uid PRIMARY KEY,
    VARCHAR(32) stock,
    INTEGER iso,
    INTEGER format,
    FOREIGN KEY (stock) REFERENCES filmStocks(uid)
);
""")

# table project
cursor.execute("""
CREATE TABLE IF NOT EXISTS projects(
    VARCHAR(32) uid PRIMARY KEY,
    TEXT name NOT NULL,
    TEXT description,
    TEXT location,
    BOOLEAN isLocationCoordinats,
    BOOLEAN isShared,
    VARCHAR(32) owner NOT NULL,
    FOREIGN KEY (owner) REFERENCES users(uid)
);
""")


# table albums
cursor.execute("""
CREATE TABLE IF NOT EXISTS albums(
    VARCHAR(32) uid PRIMARY KEY,
    TEXT name NOT NULL,
    TEXT description,
    VARCHAR(32) owner NOT NULL,
    BOOLEAN isShared,
    FOREIGN KEY (owner) REFERENCES users(uid)
);
""")


# table filmRolls
cursor.execute("""
CREATE TABLE IF NOT EXISTS filmRolls(
    VARCHAR(32) uid PRIMARY KEY,
    TEXT archivalId,
    DATE startShooting,
    DATE endShooting,
    VARCHAR(32) stock NOT NULL,
    VARCHAR(32) camera,
    VARCHAR(32) project,
    VARCHAR(32) owner NOT NULL,
    FOREIGN KEY (stock) REFERENCES filmStockVariants(uid),
    FOREIGN KEY (camera) REFERENCES cameras(uid),
    FOREIGN KEY (project) REFERENCES projects(uid),
    FOREIGN KEY (album) REFERENCES albums(uid),
    FOREIGN KEY (owner) REFERENCES users(uid)
);
""")


# table pictures
cursor.execute("""
CREATE TABLE IF NOT EXISTS pictures(
    VARCHAR(32) uid PRIMARY KEY,
    TEXT title NOT NULL,
    TEXT description,
    TEXT location,
    BOOLEAN isLocationCoordinats,
    TEXT aperture,
    TEXT shutter,
    TEXT flickrPostUrl,
    TEXT filename,
    VARCHAR(32) owner NOT NULL,
    VARCHAR(32) filmRoll,
    VARCHAR(32) album,
    VARCHAR(32) project,
    FOREIGN KEY (owner) REFERENCES users(uid),
    FOREIGN KEY (album) REFERENCES albums(uid),
    FOREIGN KEY (filmRoll) REFERENCES filmRolls(uid),
    FOREIGN KEY (project) REFERENCES projects(uid)
);
""")


# endregion init

# region: init_old
# cursor.execute("PRAGMA foreign_keys = ON;")
# cursor.execute("""
# CREATE TABLE if not exists film_stocks(
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     name TEXT NOT NULL,
#     iso INTEGER NOT NULL,
#     info TEXT,
#     type INTEGER NOT NULL,
#     format INTEGER NOT NULL
# );""")
# cursor.execute("""
# CREATE TABLE if not exists pictures(
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     description TEXT,
#     location TEXT,
#     aperture TEXT,
#     shutter TEXT,
#     posted INTEGER,
#     printed INTEGER,
#     thumbnail TEXT NOT NULL
# );""")
# cursor.execute("""
# CREATE TABLE if not exists filmrolls(
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     film INTEGER,
#     archival TEXT,
#     status INTEGER NOT NULL,
#     camera TEXT,
#     FOREIGN KEY (film) REFERENCES film_stocks(id)
# );""")
# cursor.execute("""
# CREATE TABLE if not exists pic_film_rel(
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     filmroll INTEGER,
#     picture INTEGER,
#     FOREIGN KEY (filmroll) REFERENCES filmrolls(id),
#     FOREIGN KEY (picture) REFERENCES pictures(id)
# );""")
#
# connection.commit()

# endregion init_old


def seed():
    rs = cursor.execute("SELECT * FROM film_stocks;").fetchall()
    if len(rs) == 0:
        default_rolls = [
            Film.Film(name="No Film",
                      iso=0,
                      development_info="",
                      type=Film.FilmType.UNDEFINED,
                      format=Film.FilmFormat.UNDEFINED),
            Film.Film(name="Ilford HP5+",
                      iso=400, development_info="",
                      type=Film.FilmType.BLACK_WHITE_PAN,
                      format=Film.FilmFormat.THIRTY_FIVE_MM),
            Film.Film(name="Ilford FP4+",
                      iso=125,
                      development_info="",
                      type=Film.FilmType.BLACK_WHITE_PAN,
                      format=Film.FilmFormat.THIRTY_FIVE_MM),
            Film.Film(name="Kodak Gold",
                      iso=200,
                      development_info="",
                      type=Film.FilmType.COLOR,
                      format=Film.FilmFormat.THIRTY_FIVE_MM),
            Film.Film(name="Kodak Ultramax",
                      iso=400, development_info="",
                      type=Film.FilmType.COLOR,
                      format=Film.FilmFormat.THIRTY_FIVE_MM),
            Film.Film(name="Ilford SFX",
                      iso=200,
                      development_info="",
                      type=Film.FilmType.INFRARED,
                      format=Film.FilmFormat.THIRTY_FIVE_MM),
            Film.Film(name="Harman Phoenix",
                      iso=200,
                      development_info="",
                      type=Film.FilmType.COLOR,
                      format=Film.FilmFormat.THIRTY_FIVE_MM),
            Film.Film(name="Fomapan 100",
                      iso=100,
                      development_info="",
                      type=Film.FilmType.BLACK_WHITE_PAN,
                      format=Film.FilmFormat.ONE_TWENTY)
        ]
        for film in default_rolls:
            film_stocks.create(film)
        connection.commit()


# seed()
