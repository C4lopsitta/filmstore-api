from fastapi import APIRouter

router = APIRouter()


@router.get("/{uid}")
def get_film_roll(uid: str):
    pass


@router.get("")
def get_all_film_rolls():
    pass


@router.post("")
def create_film_roll(request):
    pass


@router.put("/{uid}")
def update_film_roll(request, uid: str):
    pass


@router.delete("/{uid}")
def delete_film_roll(uid: str):
    pass
