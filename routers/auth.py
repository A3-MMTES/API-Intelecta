from fastapi import APIRouter

router = APIRouter()

@router.post("/login")
async def login():
    return {"message": "login"}

@router.post("/logout")
async def logout():
    return {"message": "logout"}

@router.post("/register") # admin
async def register():
    return {"message": "register"}