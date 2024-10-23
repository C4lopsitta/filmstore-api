import glob
import os
import subprocess
import uuid

from fastapi import FastAPI, Request, UploadFile
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse

import Db
import Routers
from Config.config import Config
from Entities import FilmRoll, FilmStock, FilmEmulsionType, DevelopmentStatus, Picture
from definitions import mime_file_extension, raw_file_types

app = FastAPI(title="FilmStore",
              description="""An API to manage Film rolls, stocks and the images you shot on them.""",
              version="1.1.0",
              license_info={
                  "name": "GNU GPLv3",
                  "url": "https://gnu.org/copyright/",
              })

config = Config(open(file="Config/config.json", mode="r"))

app.include_router(Routers.film_stocks_router)
app.include_router(Routers.film_rolls_router, prefix="/api/v1/filmRolls")
app.include_router(Routers.pictures_router, prefix="/api/v1/pictures")
app.include_router(Routers.albums_router, prefix="/api/v1/albums")
app.include_router(Routers.projects_router, prefix="/api/v1/projects")
app.include_router(Routers.cameras_router, prefix="/api/v1/cameras")
# TODO)) Users


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


@app.get("/api/v1/config")
async def get_api_config():
    return JSONResponse(
        status_code=200,
        content=config.to_dict()
    )


@app.get("/api/v1/film_rolls")
async def list_filmrolls(stock: int = 0):
    try:
        film_rolls = Db.film_rolls.fetch_all(stock_filter=stock)
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
        film_roll = Db.film_rolls.fetch(filmroll_id=roll_id)
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
        pictures = Db.pictures.fetch_all()
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
        picture = Db.pictures.fetch(picture_id=picture_id)
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
                        path=f'./pictures/{filename}.jpg')


@app.get("/api/v1/pictures/hires/{filename}")
async def get_picture(filename: str):
    if config.original_folder is None:
        return JSONResponse(status_code=400,
                            content={
                                "success": False,
                                "error": "Original file storage is disabled"
                            })

    files = glob.glob(f'{config.original_folder}{filename}.*')

    if len(files) == 0:
        return JSONResponse(status_code=404,
                            content={
                                "success": False,
                                "error": "File not found"
                            })
    file = files[0]

    return FileResponse(status_code=200,
                        media_type=
                        list(mime_file_extension.keys())[list(mime_file_extension.values()).index(file.split('.')[-1])][
                            0],
                        path=file)


@app.put("/api/v1/pictures")
async def upload_image_file(request: UploadFile):
    use_processing = True if request.headers["Filmstore-Postprocess-Negative"] in ["True", "true"] else False
    postprocessing_type = request.headers["Filmstore-Postprocess-Type"]

    if use_processing and not config.allow_raw_post_processing:
        return JSONResponse(status_code=400, content={
            "success": False,
            "error": "Postprocessing is not allowed"
        })

    if request.content_type not in mime_file_extension.keys():
        original_file_ext: str = mime_file_extension[request.content_type]

        if not config.allow_raw_upload and original_file_ext in raw_file_types.values():
            return JSONResponse(status_code=400, content={
                "success": False,
                "error": "RAW File Upload is disabled"
            })

        filename = f"{uuid.uuid4().hex}.{original_file_ext}"

        # Store temporary file for thumbnail
        with open(f"{config.temporary_files_folder}{filename}", "wb") as f:
            f.write(request.file.read())

        # Store original file if allowed
        if config.original_folder is not None:
            with open(f"{config.original_folder}{filename}", "wb") as f:
                f.write(request.file.read())

        if config.allow_raw_post_processing and use_processing:
            # TODO)) Add postprocessing
            pass

        if original_file_ext in raw_file_types.values():
            # TODO)) Add image file transform into compressed jpg
            pass
        else:
            subprocess.run(["./Scripts/create_thumbnail.sh",
                            f"{config.temporary_files_folder}{filename}",
                            f"./pictures/{filename.split('.')[0]}.jpg"])

        os.remove(f".temp/{filename}")

        return JSONResponse(status_code=201, content={
            "success": True,
            "image_filename": filename.split('.')[0],
            "thumbnail_path": f"/api/v1/pictures/file/{filename.split('.')[0]}.jpg",
            "original_file": f"/api/v1/pictures/hires/{filename}" if config.allow_raw_upload else None,
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
        insert_id = Db.pictures.create(picture=picture)
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
async def add_film_roll(request: Request):
    req_json = await request.json()

    pictures = [Picture(thumbnail="", db_id=id) for id in req_json["pictures"]]
    film = FilmStock(db_id=req_json["film"], name="", iso=0, development_info="", type=FilmEmulsionType.UNDEFINED)

    filmroll = FilmRoll(camera=req_json["camera"],
                        archival_identifier=req_json["identifier"],
                        status=DevelopmentStatus(req_json["status"]),
                        pictures=pictures,
                        film=film)

    try:
        id = Db.film_rolls.create(filmroll=filmroll)
    except Exception as e:
        return JSONResponse(status_code=500, content={
            "success": False,
            "error": str(e)
        })

    return JSONResponse(status_code=201, content={
        "success": True,
        "filmroll_id": id
    })

