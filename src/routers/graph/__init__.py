from fastapi import APIRouter
from .desk import router as desk_router
from .node import router as node_router
from .type import router as type_router
from .typology import router as typology_router
from .relationship import router as relationship_router


router = APIRouter(prefix='/graph', tags=['Graph'])

router.include_router(desk_router)
router.include_router(node_router)
router.include_router(type_router)
router.include_router(typology_router)
router.include_router(relationship_router)


@router.get('/')
def home_page():
    return 'Home graph route'
