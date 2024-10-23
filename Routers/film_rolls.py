from fastapi import APIRouter

router = APIRouter()


@router.get("/api/v1/filmRolls/{uid}")
def get_film_roll(uid: str):
    pass


@router.get("/api/v1/filmRolls")
def get_all_film_rolls():
    pass


@router.post("/api/v1/filmRolls")
def create_film_roll(request):
    pass


@router.put("/api/v1/filmRolls/{uid}")
def update_film_roll(request, uid: str):
    pass


@router.delete("/api/v1/filmRolls/{uid}")
def delete_film_roll(uid: str):
    pass
