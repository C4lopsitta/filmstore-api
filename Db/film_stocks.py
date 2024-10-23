import uuid

import Db
from Entities.FilmStock import FilmStock, FilmStockVariant


def create(film_stock: FilmStock):
    # Check existence of base stock
    if _db_load_stock(uid=film_stock.uid) is None:
        # Not there, create it
        Db.cursor.execute(f"""
            INSERT INTO filmStocks VALUES('{film_stock.uid}',
                                          '{film_stock.name}',
                                          '{film_stock.info}',
                                          {film_stock.emulsion_type.value});
        """)

        Db.connection.cursor()

    # Create all variants, if it doesn't exist
    for variant in film_stock.variants:
        if Db.cursor.execute(
                f"SELECT * FROM filmStockVariants WHERE stock = '{film_stock.uid}' AND uid = '{variant.uid}';").fetchall() is None:
            Db.cursor.execute(f"""
                INSERT INTO filmStockVariants VALUES('{variant.uid}',
                                                     '{film_stock.uid}',
                                                     {variant.iso},
                                                     {variant.format.value});
            """)

    Db.connection.commit()


def fetch(uid: str | uuid.UUID) -> FilmStock | None:
    # Check if it exists, if it's there, load it and then load the variants
    row = _db_load_stock(uid=uid)

    if row is None:
        return None

    stock_variants = _load_variants(uid=uid)
    stock = FilmStock.from_db(row=row,
                              variants=stock_variants)

    return stock


def fetch_all() -> list[FilmStock] | None:
    stocks: list[FilmStock] = []

    rows = Db.cursor.execute("SELECT * FROM filmStocks;").fetchall()

    if len(rows) == 0 or rows[0] is None:
        return None

    for row in rows:
        variants = _load_variants(uid=row[0])
        stocks.append(FilmStock.from_db(row=row, variants=variants))

    return stocks


def update(stock: FilmStock) -> None:
    if _db_load_stock(uid=stock.uid) is None:
        raise KeyError(f"Stock {stock.uid} does not exist. Create it first.")

    for variant in stock.variants:
        _update_variant(stock_uid=stock.uid,
                        variant=variant)

    Db.cursor.execute(f"""
        UPDATE filmStocks WHERE uid = '{stock.uid}' SET name = '{stock.name}', info = '{stock.info}', emulsion_type = '{stock.emulsion_type}';
    """)

    Db.connection.commit()


def delete(uid: str):
    if _db_load_stock(uid=uid) is None:
        KeyError(f"Stock {uid} does not exist. Create it first.")

    Db.cursor.execute(f"""
        DELETE FROM filmStocks WHERE uid = '{uid}';
    """)

    Db.connection.commit()


def _db_load_stock(uid: str) -> tuple:
    return Db.cursor.execute(f"SELECT * FROM filmStocks WHERE uid = '{uid}';").fetchone()


def _load_variants(uid: str) -> list[FilmStockVariant]:
    stock_variants: list[FilmStockVariant] = []

    # Get all variants
    for variant_row in Db.cursor.execute(f"SELECT * FROM filmStockVariants WHERE stock = '{uid}';"):
        stock_variants.append(FilmStockVariant.from_db(row=variant_row))

    return stock_variants


def _update_variant(stock_uid: str,
                    variant: FilmStockVariant):
    row = Db.cursor.execute(
        f"SELECT * FROM filmStockVariants WHERE stock = '{stock_uid}' AND uid = '{variant.uid}';").fetchall()

    if row is None:
        raise KeyError(f"Stock variant {variant.uid} of stock {stock_uid} does not exist. Create it first.")

    Db.cursor.execute(f"""
        UPDATE filmStockVariants WHERE stock = '{stock_uid}' AND uid = '{variant.uid}' SET iso = {variant.iso}, format = {variant.format.value};
    """)
