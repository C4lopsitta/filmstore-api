from fastapi import APIRouter

router = APIRouter()


@router.get("/api/v1/filmStocks/{uid}")
def get_film_stock(uid: str):
    pass


@router.get("/api/v1/filmStocks")
def get_all_film_stocks():
    pass


@router.post("/api/v1/filmStocks")
def create_film_stock(request):
    pass


@router.put("/api/v1/filmStocks/{uid}")
def update_film_stock(request, uid: str):
    pass


@router.delete("/api/v1/filmStocks/{uid}")
def delete_film_stock(uid: str):
    pass
