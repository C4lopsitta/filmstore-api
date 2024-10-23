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
        Db.connection.commit()

    # Create all variants, if it doesn't exist
    for variant in film_stock.variants:
        if Db.cursor.execute(
                f"SELECT * FROM filmStockVariants WHERE stock = '{film_stock.uid}' AND uid = '{variant.uid}';").fetchone() is None:
            _create_variant(variant=variant, stock_uid=film_stock.uid)


def fetch_parent_by_variant(uid: str) -> FilmStock | None:
    row = Db.cursor.execute(f"""
        SELECT * FROM filmStockVariants WHERE uid = '{uid}';
    """)

    if row is None:
        return None

    return fetch(uid=row[1])


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

    Db.cursor.execute(f"""UPDATE filmStocks
                          SET name = '{stock.name}', info = '{stock.info}', emulsionType = '{stock.emulsion_type.value}'
                          WHERE uid = '{stock.uid}';""")

    Db.connection.commit()


def delete(uid: str):
    if _db_load_stock(uid=uid) is None:
        KeyError(f"Stock {uid} does not exist. Create it first.")

    Db.cursor.execute(f"""
        DELETE FROM filmStocks WHERE uid = '{uid}';
    """)

    Db.connection.commit()


def delete_variant(stock_uid: str,
                   variant_uid: str):
    if _db_load_stock(uid=stock_uid) is None:
        KeyError(f"Stock {stock_uid} does not exist. Create it first.")

    Db.cursor.execute(f"""
        DELETE FROM filmStockVariants WHERE uid = '{variant_uid}' AND stock = '{stock_uid}';
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
        f"SELECT * FROM filmStockVariants WHERE stock = '{stock_uid}' AND uid = '{variant.uid}';").fetchone()

    if row is None:
        _create_variant(variant=variant, stock_uid=stock_uid)
    else:
        Db.cursor.execute(f"""UPDATE filmStockVariants
                              SET iso = {variant.iso}, format = {variant.format.value}
                              WHERE stock = '{stock_uid}'
                              AND uid = '{variant.uid}';""")


def _create_variant(variant: FilmStockVariant, stock_uid: str):
    Db.cursor.execute(f"""
                    INSERT INTO filmStockVariants VALUES('{variant.uid}',
                                                         '{stock_uid}',
                                                         {variant.iso},
                                                         {variant.format.value});
                """)
    Db.connection.commit()
