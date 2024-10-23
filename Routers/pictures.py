from fastapi import APIRouter

router = APIRouter()


@router.get("/api/v1/pictures/{uid}")
def get_picture(uid: str):
    pass


@router.get("/api/v1/pictures")
def get_all_pictures():
    pass


@router.post("/api/v1/pictures")
def create_picture(request):
    pass


@router.put("/api/v1/pictures/{uid}")
def update_picture(request, uid: str):
    pass


@router.delete("/api/v1/pictures/{uid}")
def delete_picture(uid: str):
    pass
