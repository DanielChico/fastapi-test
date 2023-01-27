from fastapi import APIRouter
from fastapi.security import HTTPBasic

router = APIRouter()
security = HTTPBasic()

from .v1.users import UserRoutes

UserRoutes(router, security, prefix="/users").init_routes()
