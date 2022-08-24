from fastapi import APIRouter,Depends
from middleware.dependencies import get_token_header
router = APIRouter()


@router.post("/",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},)
async def update_admin():
    return {"message": "Admin getting schwifty"}
