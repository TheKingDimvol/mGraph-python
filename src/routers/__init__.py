from fastapi import APIRouter
from .auth import router as auth_router
from .graph import router as graph_router
from .websockets import router as ws_router


router = APIRouter()

router.include_router(graph_router)
router.include_router(auth_router)
router.include_router(ws_router)


@router.get('/')
def home_page():
    return 'Home route'
