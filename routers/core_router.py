from abc import ABC, abstractmethod

from fastapi import APIRouter
from fastapi.security import HTTPBasic
from core.database import SessionLocal


class CoreRouter(ABC):
    router: APIRouter
    security: HTTPBasic

    def __init__(self, router: APIRouter, security: HTTPBasic, prefix: str = ""):
        self.security = security
        self.router = router
        router.prefix = prefix

    # Dependency
    @staticmethod
    def get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    @abstractmethod
    def init_routes(self):
        pass
