from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from core.models import user_model
from routers.router import router
import uvicorn
from core.database import engine


user_model.Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, log_level="info", reload=True)
