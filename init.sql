PRAGMA foreign_keys = ON;

CREATE TABLE if not exists films(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    iso INTEGER NOT NULL,
    info TEXT,
    type INTEGER NOT NULL,
    format INTEGER
);

CREATE TABLE if not exists pictures(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT,
    location TEXT,
    aperture TEXT,
    shutter TEXT,
    posted INTEGER,
    printed INTEGER,
    thumbnail TEXT NOT NULL
);

CREATE TABLE if not exists filmrolls(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    film INTEGER,
    archival TEXT,
    status INTEGER NOT NULL,
    camera TEXT,
    FOREIGN KEY (film) REFERENCES films(id)
);

CREATE TABLE if not exists pic_film_rel(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filmroll INTEGER,
    picture INTEGER,
    FOREIGN KEY (filmroll) REFERENCES filmrolls(id),
    FOREIGN KEY (picture) REFERENCES pictures(id)
);
