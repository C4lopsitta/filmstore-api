import json
import os
import subprocess
import uuid

from fastapi import FastAPI, Request, UploadFile, Form
from fastapi.responses import JSONResponse
from starlette.responses import HTMLResponse

import db
from Entities.Film import Film, FilmType, FilmFormat
from Entities.FilmRoll import FilmRoll, DevelopmentStatus
from Entities.Picture import Picture

app = FastAPI()

@app.get("/")
async def root():
    return HTMLResponse(content="""
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
        "status": 200,
        "message": "Everything is working!"
    })


@app.get("/api/v1/films")
async def list_films():
    try:
        films = db.fetch_films()
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content={
            "status": 500,
            "message": str(e)
        })

    json_films = [film.to_dict() for film in films]

    return JSONResponse(status_code=200, content={
        "status": 200,
        "message": "Successfully fetched films",
        "films": json_films
    })


@app.get("/api/v1/films/{film_id}")
async def get_film(film_id: int):
    try:
        film = db.fetch_film(film_id=film_id)
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content={
            "status": 500,
            "message": str(e)
        })

    return JSONResponse(status_code=200, content={
        "status": 200,
        "message": "Successfully fetched film",
        "film": film.to_dict()
    })


@app.get("/api/v1/filmrolls")
async def list_filmrolls():
    try:
        filmrolls = db.fetch_filmrolls()
    except Exception as e:
        print(e)
        return JSONResponse(status_code=500, content={
            "status": 500,
            "message": str(e)
        })

    return JSONResponse(status_code=200, content={
        "status": 200,
        "message": "Successfully fetched filmrolls",
        "filmrolls": [filmroll.to_dict() for filmroll in filmrolls]
    })


@app.get("/api/v1/filmrolls/{filmrollid}")
async def get_filmroll(filmrollid: int):
    filmroll = db.fetch_filmroll(filmrollid)

    return JSONResponse(status_code=200, content={
        "status": 200,
        "message": "Successfully fetched filmroll",
        "id": filmrollid,
        "film": filmroll.film.to_dict(),
        "pictures": [picture.db_id for picture in filmroll.pictures],
        "filmroll_status": filmroll.status,
        "camera": filmroll.camera,
        "identifier": filmroll.archival_identifier
    })


@app.get("/api/v1/pictures/{pictureid}")
async def get_picture(pictureid: int):
    return JSONResponse(status_code=200, content={})


@app.post("/api/v1/films")
async def create_film(request: Request):
    req_json = await request.json()

    film = Film(name=req_json["name"],
                iso=req_json["iso"],
                development_info=req_json["development_info"],
                type=FilmType(req_json["type"]),
                format=FilmFormat(req_json["format"]))

    try:
        db.add_film(film)
    except Exception as e:
        return JSONResponse(status_code=500, content={
            "status": 500,
            "message": str(e)
        })
    return JSONResponse(status_code=200, content={
        "status": 200,
        "message": "Film created",
        "request_json": req_json
    })


# Consider switch to base64 in json for simplicity reasons
@app.post("/api/v1/pictures")
async def upload_picture(file: UploadFile, req: str = Form()):
    req_json = json.loads(req)

    if file.content_type == 'image/jpeg' or file.content_type == 'image/png':
        # Run compression script
        filename = f"{uuid.uuid4().hex}."
        filename += "jpeg" if file.content_type == 'image/jpeg' else "png"
        with open(".temp/" + filename, 'wb') as f:
            f.write(await file.read())

        subprocess.run(
            ["./scripts/img.sh", f".temp/{filename}", f"./pictures/{filename}"]
        )
    else: # TODO)) ADD FILM FORMAT
        return JSONResponse(status_code=400,
                            content={
                                "status": 400,
                                "message": "Only JPEG and PNG are supported"
                            })

    picture = Picture(thumbnail=filename,
                      description=req_json["description"],
                      location=req_json["location"],
                      aperture=req_json["aperture"],
                      shutter_speed=req_json["shutter_speed"],
                      posted=req_json["posted"],
                      printed=req_json["printed"])

    try:
        insert_id = db.add_picture(picture)
    except Exception as e:
        return JSONResponse(status_code=500, content={
            "status": 500,
            "message": str(e)
        })

    return JSONResponse(status_code=200, content={
        "status": 200,
        "message": "Picture stored successfully!",
        "picture_id": insert_id
    })


@app.post("/api/v1/filmrolls")
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
        id = db.add_filmroll(filmroll)
    except Exception as e:
        return JSONResponse(status_code=500, content={
            "status": 500,
            "message": str(e)
        })

    return JSONResponse(status_code=200, content={
        "status": 200,
        "message": "Filmroll added",
        "filmroll_id": id
    })

@app.post("/api/v1/films/{id}")
async def update_film(request: Request, id: int):
    pass

@app.delete("/api/v1/films/{id}")
async def delete_film(id: int):
    resp_json = db.fetch_film(id).to_dict()

    pictures_to_delete, deleted_films = db.delete_film_stock(id)
    for picture in pictures_to_delete:
        os.remove(f"./pictures/{picture}")

    return JSONResponse(status_code=200, content={
        "status": 200,
        "message": f"Film deleted successfully along {deleted_films} film rolls and {len(pictures_to_delete)} pictures",
    })
