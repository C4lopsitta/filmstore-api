from fastapi import APIRouter
from fastapi.responses import JSONResponse

import Db
from Entities import FilmStock, FilmStockVariant

router = APIRouter()


@router.get("/api/v1/filmStocks/{uid}")
def get_film_stock(uid: str):
    stock = Db.film_stocks.fetch(uid)
    if stock is None:
        return JSONResponse(status_code=404,
                            content={
                                "success": False,
                                "error": f"Stock {uid} not found"
                            })

    return JSONResponse(status_code=200,
                        content={
                            "success": True,
                            "stock": stock.to_dict()
                        })


@router.get("/api/v1/filmStocks/variant/{uid}")
def get_film_stock_variant(uid: str):
    stock = Db.film_stocks.fetch_parent_by_variant(uid)

    if stock is None:
        return JSONResponse(status_code=404,
                            content={
                                "success": False,
                                "error": f"Stock variant {uid} not found"
                            })

    return JSONResponse(status_code=200,
                        content={
                            "success": True,
                            "stock": stock.to_dict()
                        })


@router.get("/api/v1/filmStocks")
def get_all_film_stocks():
    stocks = Db.film_stocks.fetch_all()

    status_code = 204 if stocks is None or len(stocks) == 0 else 200

    return JSONResponse(status_code=status_code,
                        content={
                            "success": True,
                            "stocks": [stock.to_dict() for stock in stocks]
                        })


@router.post("/api/v1/filmStocks")
async def create_film_stock(request):
    # TODO)) Add auth check
    request_json = await request.json()

    try:
        stock_variants: list[FilmStockVariant] = []
        for variant in request_json["variants"]:
            stock_variants.append(FilmStockVariant(**variant))

        stock = FilmStock(**request_json, variants=stock_variants)
    except Exception as e:
        return JSONResponse(status_code=400,
                            content={
                                "success": False,
                                "error": str(e)
                            })

    try:
        Db.film_stocks.create(stock)
    except Exception as e:
        return JSONResponse(status_code=500,
                            content={
                                "success": False,
                                "error": str(e)
                            })

    return JSONResponse(status_code=201,
                        content={
                            "success": True,
                            "stock": stock.to_dict()
                        })


@router.put("/api/v1/filmStocks/{uid}")
async def update_film_stock(request, uid: str):
    request_json = await request.json()

    try:
        stock_variants: list[FilmStockVariant] = []

        for variant in request_json["variants"]:
            stock_variants.append(FilmStockVariant(**variant))

        stock = FilmStock(**request_json)
    except Exception as e:
        return JSONResponse(status_code=400,
                            content={
                                "success": False,
                                "error": str(e)
                            })

    try:
        Db.film_stocks.update(stock)
    except Exception as e:
        return JSONResponse(status_code=500,
                            content={
                                "success": False,
                                "error": str(e)
                            })

    return JSONResponse(status_code=200,
                        content={
                            "success": True,
                            "stock": stock.to_dict()
                        })


@router.delete("/api/v1/filmStocks/{uid}")
def delete_film_stock(uid: str):
    try:
        Db.film_stocks.delete(uid)
    except KeyError as kerr:
        return JSONResponse(status_code=400,
                            content={
                                "success": False,
                                "error": f"Stock {uid} not found"
                            })
    except Exception as e:
        return JSONResponse(status_code=500,
                            content={
                                "success": False,
                                "error": str(e)
                            })

    return JSONResponse(status_code=200,
                        content={
                            "success": True
                        })
