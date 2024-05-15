from fastapi import APIRouter
from posts.services import create_post

router = APIRouter(prefix="/posts", tags=["users"])

# Путь '/create/' будет добавлен к префиксу '/posts',
# что дает полный путь '/posts/create/'.
# Функция create_post будет вызываться при обращении к этому пути.

router.post("/create/")(create_post)
