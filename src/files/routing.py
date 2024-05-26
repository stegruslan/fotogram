from fastapi import APIRouter
from files.services import get_file

router = APIRouter(prefix="/files", tags=["files"])
# Создаем маршрутизатор с префиксом "/files" и тегом "files".
router.get("/{filename}")(get_file)
# Определяем маршрут для GET-запросов к файлам по имени файла.
# Когда запрос поступает на /files/{filename}, вызывается функция get_file.
