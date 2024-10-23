from fastapi import APIRouter

router = APIRouter()


@router.get("/api/v1/albums/{uid}")
def get_album(uid: str):
    pass


@router.get("/api/v1/albums")
def get_all_albums():
    pass


@router.post("/api/v1/albums")
def create_album(request):
    pass


@router.put("/api/v1/albums/{uid}")
def update_album(request, uid: str):
    pass


@router.delete("/api/v1/albums/{uid}")
def delete_album(uid: str):
    pass
