import json
import subprocess
import uuid

from fastapi import FastAPI, Request, UploadFile, Form
from fastapi.responses import JSONResponse

import db
from Entities.Film import Film, FilmType
from Entities.FilmRoll import FilmRoll, DevelopmentStatus
from Entities.Picture import Picture

app = FastAPI()


@app.get("/")
async def root():
    return JSONResponse(status_code=200, content={
        "status": 200,
        "message": "Everything is working!"
    })


@app.get("/films")
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


@app.get("/films/{film_id}")
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


@app.get("/filmrolls")
async def list_filmrolls():
    return JSONResponse(status_code=200, content={})


@app.get("/filmrolls/{filmrollid}")
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


@app.get("/pictures/{pictureid}")
async def get_picture(pictureid: int):
    return JSONResponse(status_code=200, content={})


@app.post("/films")
async def create_film(request: Request):
    req_json = await request.json()

    film = Film(name=req_json["name"],
                iso=req_json["iso"],
                development_info=req_json["development_info"],
                type=FilmType(req_json["type"]))

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


@app.post("/pictures")
async def upload_picture(file: UploadFile, req: str = Form()):
    req_json = json.loads(req)

    if file.content_type == 'image/jpeg':
        # Run compression script
        filename = f"{uuid.uuid4().hex}.jpeg"
        with open(".temp/" + filename, 'wb') as f:
            f.write(await file.read())

        subprocess.run(
            ["./scripts/jpeg.sh", f".temp/{filename}", f"./pictures/{filename}"]
        )
    else:
        return JSONResponse(status_code=400,
                            content={
                                "status": 400,
                                "message": "Only JPEG is supported"
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


@app.post("/filmrolls")
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
