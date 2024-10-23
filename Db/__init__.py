import sqlite3

from Config.config import Config
from Db import albums, cameras, film_rolls, film_stocks, pictures, projects, users

config = Config(open(file="Config/config.json", mode="r"))
connection = sqlite3.connect(config.database_file_name)

cursor = connection.cursor()

# region init
cursor.execute("PRAGMA foreign_keys=ON;")

# table users
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    uid VARCHAR(32) PRIMARY KEY,
    username VARCHAR(32) UNIQUE NOT NULL,
    passwordHash TEXT NOT NULL
);
""")
# table cameras
cursor.execute("""
CREATE TABLE IF NOT EXISTS cameras(
    uid VARCHAR(32) PRIMARY KEY,
    owner VARCHAR(32) NOT NULL,
    brand TEXT NOT NULL,
    model TEXT,
    format INTEGER NOT NULL,    
    FOREIGN KEY (owner) REFERENCES users(uid) ON DELETE CASCADE
)
""")
# table filmStocks
cursor.execute("""
CREATE TABLE IF NOT EXISTS filmStocks(
    uid VARCHAR(32) PRIMARY KEY,
    name TEXT NOT NULL,
    info TEXT,
    emulsionType INTEGER NOT NULL
);
""")
# table filmStockVariant
cursor.execute("""
CREATE TABLE IF NOT EXISTS filmStockVariants(
    uid VARCHAR(32) PRIMARY KEY,
    stock VARCHAR(32) NOT NULL,
    iso INT NOT NULL,
    format INTEGER NOT NULL,
    FOREIGN KEY (stock) REFERENCES filmStocks(uid) ON DELETE CASCADE
);
""")
# table project
cursor.execute("""
CREATE TABLE IF NOT EXISTS projects(
    uid VARCHAR(32) PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    location TEXT,
    isLocationCoordinates BOOLEAN DEFAULT false,
    isShared BOOLEAN DEFAULT false,
    owner VARCHAR(32) NOT NULL,
    FOREIGN KEY (owner) REFERENCES users(uid) ON DELETE CASCADE
);
""")
# table albums
cursor.execute("""
CREATE TABLE IF NOT EXISTS albums(
    uid VARCHAR(32) PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    owner VARCHAR(32) NOT NULL,
    isShared BOOLEAN DEFAULT false,
    FOREIGN KEY (owner) REFERENCES users(uid) ON DELETE CASCADE
);
""")
# table filmRolls
cursor.execute("""
CREATE TABLE IF NOT EXISTS filmRolls(
    uid VARCHAR(32) PRIMARY KEY,
    archivalId TEXT,
    startShooting DATE,
    endShooting DATE,
    stock VARCHAR(32) NOT NULL,
    camera VARCHAR(32),
    project VARCHAR(32),
    album VARCHAR(32),
    owner VARCHAR(32) NOT NULL,
    isShared BOOLEAN DEFAULT false,
    FOREIGN KEY (stock) REFERENCES filmStockVariants(uid) ON DELETE CASCADE,
    FOREIGN KEY (camera) REFERENCES cameras(uid) ON DELETE SET NULL ,
    FOREIGN KEY (project) REFERENCES projects(uid) ON DELETE SET NULL,
    FOREIGN KEY (album) REFERENCES albums(uid) ON DELETE SET NULL,
    FOREIGN KEY (owner) REFERENCES users(uid) ON DELETE CASCADE
);
""")
# table pictures
cursor.execute("""
CREATE TABLE IF NOT EXISTS pictures(
    uid VARCHAR(32) PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    location TEXT,
    isLocationCoordinates BOOLEAN DEFAULT false,
    aperture TEXT,
    shutter TEXT,
    flickrPostUrl TEXT,
    filename TEXT,
    owner VARCHAR(32) NOT NULL,
    filmRoll VARCHAR(32),
    album VARCHAR(32),
    project VARCHAR(32),
    FOREIGN KEY (owner) REFERENCES users(uid) ON DELETE CASCADE,
    FOREIGN KEY (album) REFERENCES albums(uid) ON DELETE SET NULL,
    FOREIGN KEY (filmRoll) REFERENCES filmRolls(uid) ON DELETE SET NULL,
    FOREIGN KEY (project) REFERENCES projects(uid) ON DELETE SET NULL
);
""")
# endregion init

#
# def seed():
#     rs = cursor.execute("SELECT * FROM filmStocks;").fetchall()
#     if len(rs) == 0:
#         default_rolls = [
#             Film.FilmStock(name="No Film",
#                            iso=0,
#                            development_info="",
#                            type=Film.FilmEmulsionType.UNDEFINED,
#                            format=Film.FilmFormat.UNDEFINED),
#             Film.FilmStock(name="Ilford HP5+",
#                            iso=400, development_info="",
#                            type=Film.FilmEmulsionType.BLACK_WHITE_PAN,
#                            format=Film.FilmFormat.THIRTY_FIVE_MM),
#             Film.FilmStock(name="Ilford FP4+",
#                            iso=125,
#                            development_info="",
#                            type=Film.FilmEmulsionType.BLACK_WHITE_PAN,
#                            format=Film.FilmFormat.THIRTY_FIVE_MM),
#             Film.FilmStock(name="Kodak Gold",
#                            iso=200,
#                            development_info="",
#                            type=Film.FilmEmulsionType.COLOR,
#                            format=Film.FilmFormat.THIRTY_FIVE_MM),
#             Film.FilmStock(name="Kodak Ultramax",
#                            iso=400, development_info="",
#                            type=Film.FilmEmulsionType.COLOR,
#                            format=Film.FilmFormat.THIRTY_FIVE_MM),
#             Film.FilmStock(name="Ilford SFX",
#                            iso=200,
#                            development_info="",
#                            type=Film.FilmEmulsionType.INFRARED,
#                            format=Film.FilmFormat.THIRTY_FIVE_MM),
#             Film.FilmStock(name="Harman Phoenix",
#                            iso=200,
#                            development_info="",
#                            type=Film.FilmEmulsionType.COLOR,
#                            format=Film.FilmFormat.THIRTY_FIVE_MM),
#             Film.FilmStock(name="Fomapan 100",
#                            iso=100,
#                            development_info="",
#                            type=Film.FilmEmulsionType.BLACK_WHITE_PAN,
#                            format=Film.FilmFormat.ONE_TWENTY)
#         ]
#         for film in default_rolls:
#             film_stocks.create(film)
#         connection.commit()
#
#     rs = connection.execute("SELECT * FROM users;").fetchall()
#     if len(rs) == 0:
#         connection.execute(f"INSERT INTO users VALUES({uuid.uuid4().__str__()},"
#                            f"'DEFAULT', '')")
#
# seed()
