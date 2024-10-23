from fastapi import APIRouter

router = APIRouter()


@router.get("/{uid}")
def get_album(uid: str):
    pass


@router.get("")
def get_all_albums():
    pass


@router.post("")
def create_album(request):
    pass


@router.put("/{uid}")
def update_album(request, uid: str):
    pass


@router.delete("/{uid}")
def delete_album(uid: str):
    pass
