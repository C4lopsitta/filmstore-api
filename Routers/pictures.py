from fastapi import APIRouter

router = APIRouter()


@router.get("/{uid}")
def get_picture(uid: str):
    pass


@router.get("")
def get_all_pictures():
    pass


@router.post("")
def create_picture(request):
    pass


@router.put("/{uid}")
def update_picture(request, uid: str):
    pass


@router.delete("/{uid}")
def delete_picture(uid: str):
    pass
