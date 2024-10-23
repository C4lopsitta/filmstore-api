from fastapi import APIRouter

router = APIRouter()


@router.get("/api/v1/projects/{uid}")
def get_project(uid: str):
    pass


@router.get("/api/v1/projects")
def get_all_projects():
    pass


@router.post("/api/v1/projects")
def create_project(request):
    pass


@router.put("/api/v1/projects/{uid}")
def update_project(request, uid: str):
    pass


@router.delete("/api/v1/projects/{uid}")
def delete_project(uid: str):
    pass
