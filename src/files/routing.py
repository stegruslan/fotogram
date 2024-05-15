from fastapi import APIRouter
from files.services import get_file

router = APIRouter(prefix="/files", tags=["files"])
router.get("/{filename}")(get_file)
