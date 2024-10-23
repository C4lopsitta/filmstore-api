from fastapi import APIRouter

router = APIRouter()


@router.get("/{uid}")
def get_project(uid: str):
    pass


@router.get("")
def get_all_projects():
    pass


@router.post("")
def create_project(request):
    pass


@router.put("/{uid}")
def update_project(request, uid: str):
    pass


@router.delete("/{uid}")
def delete_project(uid: str):
    pass
