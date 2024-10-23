from fastapi import APIRouter

router = APIRouter()


@router.get("/{uid}")
def get_camera(uid: str):
    pass


@router.get("")
def get_all_cameras():
    pass


@router.post("")
def create_camera(request):
    pass


@router.put("/{uid}")
def update_camera(request, uid: str):
    pass


@router.delete("/{uid}")
def delete_camera(uid: str):
    pass
