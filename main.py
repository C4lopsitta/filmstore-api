import json
import os
import subprocess
import uuid

from fastapi import FastAPI, Request, UploadFile, Form
from fastapi.responses import JSONResponse, FileResponse
from starlette.responses import HTMLResponse

import db
from BaseModels.Films import FilmsBaseModel
from Entities.Film import Film, FilmType, FilmFormat
from Entities.FilmRoll import FilmRoll, DevelopmentStatus
from Entities.Picture import Picture
from config.config import Config
from definitions import mime_file_extension

app = FastAPI(title="FilmStore",
              description="""An API to manage Film rolls, stocks and the images you shot on them.""",
              version="1.0.0",
              license_info={
                "name": "GNU GPLv3",
                "url": "https://gnu.org/copyright/",
              })
config = Config(open(file="./config/config.json", mode="r"))


@app.get("/")
async def root():
    return HTMLResponse(status_code=200, content="""
    <!DOCTYPE html>
    <html>
        <head>
            <meta charset="utf-8">
            <title>Filmstore</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
        </head>
        <body>
            <h1>Filmstore</h1>
            <p>Everything should be working</p>
        </body>
    </html>
    """)


@app.get("/api/v1")
async def api_root():
    return JSONResponse(status_code=200, content={
        "success": True,
        "status": "Everything is working!",
        "api_version": "1.0.0"
    })


@app.get("/api/v1/film_stocks")
async def list_films():
    try:
        films = db.film_stocks.fetch_all()
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content={
            "success": False,
            "error": str(e)
        })

    json_films = [film.to_dict() for film in films]

    return JSONResponse(status_code=200, content={
        "success": True,
        "films": json_films
    })


@app.get("/api/v1/film_stocks/{film_id}")
async def get_film(film_id: int):
    try:
        film = db.film_stocks.fetch(film_id=film_id)
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content={
            "success": False,
            "error": str(e)
        })

    return JSONResponse(status_code=200, content={
        "success": True,
        "film": film.to_dict()
    })


@app.get("/api/v1/film_rolls")
async def list_filmrolls(stock: int = 0):
    try:
        film_rolls = db.film_rolls.fetch_all(stock_filter=stock)
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content={
            "success": False,
            "error": str(e)
        })

    return JSONResponse(status_code=200, content={
        "success": True,
        "filmrolls": [filmroll.to_dict() for filmroll in film_rolls]
    })


@app.get("/api/v1/film_rolls/{filmrollid}")
async def get_film_roll(roll_id: int):
    try:
        film_roll = db.film_rolls.fetch(filmroll_id=roll_id)
    except Exception as e:
        return JSONResponse(status_code=500, content={"success": False, "error": str(e)})

    return JSONResponse(status_code=200, content={
        "success": True,
        "id": roll_id,
        "film": film_roll.film.to_dict(),
        "pictures": [picture.db_id for picture in film_roll.pictures],
        "filmroll_status": film_roll.status,
        "camera": film_roll.camera,
        "identifier": film_roll.archival_identifier
    })


@app.get("/api/v1/pictures")
async def list_pictures():
    try:
        pictures = db.pictures.fetch_all()
    except Exception as e:
        return JSONResponse(status_code=500, content={"success": False, "error": str(e)})

    pictures_jsons = []
    for picture in pictures:
        pictures_jsons.append(picture.to_dict())
        print(picture)

    return JSONResponse(status_code=200, content={
        "success": True,
        "pictures": pictures_jsons
    })


@app.get("/api/v1/pictures/{picture_id}")
async def get_picture(picture_id: int):
    try:
        picture = db.pictures.fetch(picture_id=picture_id)
    except Exception as e:
        return JSONResponse(status_code=500, content={"success": False, "error": str(e)})
    return JSONResponse(status_code=200, content={
        "success": True,
        "id": picture.db_id,
        "thumbnail": picture.thumbnail,
        "description": picture.description,
        "location": picture.location,
        "aperture": picture.aperture,
        "shutter_speed": picture.shutter_speed,
        "posted": picture.posted,
        "printed": picture.printed,
    })


@app.get("/api/v1/pictures/file/{filename}")
async def get_picture(filename: str):
    return FileResponse(status_code=200,
                        media_type='image/jpeg',
                        path=f'./pictures/{filename}')


@app.post("/api/v1/film_stocks")
async def create_film(request: FilmsBaseModel):
    film = Film(name=request.name,
                iso=request.iso,
                development_info=request.development_info,
                type=FilmType(request.type),
                format=FilmFormat(request.format),)

    # TODO)) ADD id and response id
    try:
        db_id = db.film_stocks.create(film=film)
    except Exception as e:
        return JSONResponse(status_code=500, content={
            "message": str(e)
        })
    return JSONResponse(status_code=201, content={
        "success": True,
        "film_id": db_id,
    })


@app.put("/api/v1/pictures")
async def upload_image_file(request: UploadFile):
    if request.content_type not in mime_file_extension.keys():
        tempfile_ext: str = mime_file_extension[request.content_type]

        filename = f"{uuid.uuid4().hex}.{tempfile_ext}"

        with open(f"{config.temporary_files_folder}{filename}", "wb") as f:
            f.write(request.file.read())

        subprocess.run(
            ["./scripts/img.sh", f"{config.temporary_files_folder}{filename}", f"./pictures/{filename.split('.')[0]}.jpg"],
        )

        os.remove(f".temp/{filename}")

        return JSONResponse(status_code=200, content={
            "success": True,
            "image_filename": filename,
            "thumbnail_path": f"/api/v1/pictures/file/{filename}",
            "original_file": f"",
            "awaiting_metadata": True
        })
    else:
        return JSONResponse(status_code=400, content={
            "success": False,
            "error": f"Image formats supported are {mime_file_extension.values()}\nSent file uses {request.content_type}"
        })


@app.post("/api/v1/pictures")
async def upload_picture(request):
    req_json = await request.json()

    # else:  # TODO)) ADD FILM FORMAT

    picture = Picture(thumbnail="",
                      description=req_json["description"],
                      location=req_json["location"],
                      aperture=req_json["aperture"],
                      shutter_speed=req_json["shutter_speed"],
                      posted=req_json["posted"],
                      printed=req_json["printed"])

    try:
        insert_id = db.pictures.create(picture=picture)
    except Exception as e:
        return JSONResponse(status_code=500, content={
            "success": False,
            "error": str(e)
        })

    return JSONResponse(status_code=201, content={
        "success": True,
        "picture_id": insert_id
    })


@app.post("/api/v1/film_rolls")
async def add_filmroll(request: Request):
    req_json = await request.json()

    pictures = [Picture(thumbnail="", db_id=id) for id in req_json["pictures"]]
    film = Film(db_id=req_json["film"], name="", iso=0, development_info="", type=FilmType.UNDEFINED)

    filmroll = FilmRoll(camera=req_json["camera"],
                        archival_identifier=req_json["identifier"],
                        status= DevelopmentStatus(req_json["status"]),
                        pictures=pictures,
                        film=film)

    try:
        id = db.film_rolls.create(filmroll=filmroll)
    except Exception as e:
        return JSONResponse(status_code=500, content={
            "success": False,
            "error": str(e)
        })

    return JSONResponse(status_code=201, content={
        "success": True,
        "filmroll_id": id
    })


@app.post("/api/v1/film_stocks/{id}")
async def update_film(request: Request, id: int):
    pass


@app.delete("/api/v1/film_stocks/{id}")
async def delete_film(stock_id: int):
    try:
        resp_json = db.film_stocks.delete(film_stock_id=stock_id)
    except Exception as e:
        return JSONResponse(status_code=500, content={"success": False, "error": str(e)})

    resp_json.update({"success": True})
    return JSONResponse(status_code=200, content=resp_json)
