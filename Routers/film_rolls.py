from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.requests import Request

import Db
from Entities import FilmRoll

router = APIRouter()


@router.get("/{uid}")
def get_film_roll(uid: str):
    try:
        film_roll = Db.film_rolls.fetch(uid=uid)
    except Exception as e:
        return JSONResponse(status_code=500,
                            content={
                                "success": False,
                                "error": e.__str__()
                            })

    if film_roll is None:
        return JSONResponse(status_code=404,
                            content={
                                "success": False,
                                "error": f"Film roll {uid} not found"
                            })

    return JSONResponse(status_code=200,
                        content={
                            "success": True,
                            "film_roll": film_roll.to_dict()
                        })


@router.get("")
def get_all_film_rolls(stock_filter: str | None = None):
    try:
        film_rolls = Db.film_rolls.fetch_all(stock_filter=stock_filter)
    except Exception as e:
        return JSONResponse(status_code=500,
                            content={
                                "success": False,
                                "error": e.__str__()
                            })

    response_status_code = 204 if film_rolls is None or len(film_rolls) == 0 else 200
    film_rolls = film_rolls if film_rolls is not None else []
    return JSONResponse(status_code=response_status_code,
                        content={
                            "success": True,
                            "rolls": [film_roll.to_dict() for film_roll in film_rolls]
                        })


@router.post("")
async def create_film_roll(request: Request):
    # TODO)) Auth
    # TODO)) Check existence of FK
    request_json = await request.json()

    try:
        film_roll = FilmRoll(**request_json)
    except Exception as e:
        return JSONResponse(status_code=400,
                            content={
                                "success": False,
                                "error": e.__str__()
                            })

    try:
        Db.film_rolls.create(film_roll)
    except Exception as e:
        return JSONResponse(status_code=500,
                            content={
                                "success": False,
                                "error": e.__str__()
                            })

    return JSONResponse(status_code=201,
                        content={
                            "success": True,
                            "film_roll": film_roll.to_dict()
                        })


@router.put("/{uid}")
async def update_film_roll(request: Request, uid: str):
    # TODO)) Auth
    # TODO)) Check existence of FK
    request_json = await request.json()

    try:
        film_roll = FilmRoll(**request_json)
    except Exception as e:
        return JSONResponse(status_code=400,
                            content={
                                "success": False,
                                "error": e.__str__()
                            })

    try:
        Db.film_rolls.update(film_roll=film_roll)
    except Exception as e:
        return JSONResponse(status_code=500,
                            content={
                                "success": False,
                                "error": e.__str__()
                            })

    return JSONResponse(status_code=200,
                        content={
                            "success": True,
                            "film_roll": film_roll.to_dict()
                        })


@router.delete("/{uid}")
def delete_film_roll(uid: str):
    try:
        Db.film_rolls.delete(uid=uid)
    except KeyError as kerr:
        return JSONResponse(status_code=404,
                            content={
                                "success": False,
                                "error": f"Film Roll {uid} does not exist"
                            })
    except Exception as e:
        return JSONResponse(status_code=500,
                            content={
                                "success": False,
                                "error": e.__str__()
                            })

    return JSONResponse(status_code=200,
                        content={
                            "success": True
                        })
