from fastapi import APIRouter

router = APIRouter(
    prefix="/user",
    tags=["User"],
)


@router.post("/add/{username}")
async def add_user(username: str):
    return {"status": f"user {username} has been added"}


@router.post("/remove/{username}")
async def remove_user(username: str):
    return {"status": f"user {username} has been removed"}
