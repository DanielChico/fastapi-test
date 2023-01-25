from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from routers.v1 import users
import uvicorn



app = FastAPI()
app.include_router(users.router)
if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, log_level="info", reload=True)
