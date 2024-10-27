import os
import uuid

from fastapi import APIRouter, UploadFile, Request
from fastapi.responses import JSONResponse, FileResponse

from Config.config import Config
from Entities.Picture import ImageMimeType

router = APIRouter()
config = Config(open(file="Config/config.json", mode="r"))


@router.get("/{uid}")
def get_picture_meta(uid: str):
    pass


@router.get("")
def get_all_pictures_meta():
    pass


@router.get("/thumbnails/{uid}")
def get_picture_thumbnail(uid: str):
    pass


@router.get("/originals/{uid}")
def get_picture_original(uid: str):
    pass


@router.post("")
async def create_picture_meta(request: Request):
    request_json = await request.json()

    if request_json["uid"] is None:
        return JSONResponse(status_code=406,
                            content={
                                "success": False,
                                "error": "No UID has been provided. You need to first upload an image and follow up the image post with the metadata JSON containing the image's UID."
                            })

    pass


@router.post("/originals")
def upload_picture(request: UploadFile):
    picture_uid = uuid.uuid4().__str__()
    try:
        image_mime = ImageMimeType.from_str(request.content_type)
    except:
        return JSONResponse(status_code=415,
                            content={
                                "success": False,
                                "error": f"{request.content_type} is not a supported format. Supported formats are {ImageMimeType.__members__.values()}"
                            })

    post_processing_type = request.headers.get("Filmstore-Post-Processing-Type")
    if post_processing_type is not None:
        if not config.allow_raw_post_processing:
            return JSONResponse(status_code=406,
                                content={
                                    "success": False,
                                    "error": "Server does not allow RAW image post processing."
                                })
        pass  # TODO)) Add processing

    temp_file_name = f"{config.temporary_files_folder}/{picture_uid}.{image_mime.extension}"
    thumbnail_file_name = f"{config.temporary_files_folder}/{picture_uid}.{ImageMimeType.JPEG.value.extension}"
    original_file_name = f"{config.original_folder}/{picture_uid}.{image_mime.extension}"

    # Store original file in temporary folder
    with open(temp_file_name, "wb") as f:
        f.write(request.file.read())

    

    # remove temp file
    os.remove(temp_file_name)


    return JSONResponse(status_code=204,
                        content={
                            "success": True,
                            "picture_uid": picture_uid,
                            "continue": f"/api/v1/pictures/{picture_uid}"
                        })


@router.put("/{uid}")
def update_picture_meta(request: Request,
                        uid: str):
    pass


@router.delete("/{uid}")
def delete_picture_meta_file(uid: str):
    pass
