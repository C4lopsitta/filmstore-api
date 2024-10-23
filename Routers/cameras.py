from fastapi import APIRouter

router = APIRouter()


@router.get("/api/v1/cameras/{uid}")
def get_camera(uid: str):
    pass


@router.get("/api/v1/cameras")
def get_all_cameras():
    pass


@router.post("/api/v1/cameras")
def create_camera(request):
    pass


@router.put("/api/v1/cameras/{uid}")
def update_camera(request, uid: str):
    pass


@router.delete("/api/v1/cameras/{uid}")
def delete_camera(uid: str):
    pass
