
import logging
from logging.handlers import RotatingFileHandler
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.src.api import auth_endpoints
from app.src.util.db import Base, engine
from app.src.api.user_endpoints import UserEndpoints
from app.src.controller.user_controller import UserController


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    logging.debug("Running async DB startup init")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    # Shutdown logic (if needed)
    logging.debug("App is shutting down...")

def init():
    console_handler = logging.StreamHandler()
    file_handler = RotatingFileHandler(filename="logs/log.log", maxBytes=1e8, backupCount=5)

    logging.basicConfig(format='%(levelname)s [%(asctime)s]: %(message)s (Line: %(lineno)d [%(filename)s])',
                        datefmt='%Y.%m.%d %I:%M:%S %p',
                        # filename="logs/log.log",
                        # filemode='w',
                        level=logging.DEBUG,
                        handlers=[console_handler, file_handler])

    
    # Setting Up Logging
    logging.debug("Creating FastApi App")
    app = FastAPI(lifespan=lifespan)

    # Allow all origins (replace "*" with your frontend URL in production)
    origins = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


    user_controller = UserController()
    user_endpoints = UserEndpoints(user_controller)

    app.include_router(user_endpoints.router)
    app.include_router(auth_endpoints.router)

    return app

def start_program():

    uvicorn.run("app.main:init", host="0.0.0.0", port=8000, reload="True", factory=True)

    return 0

if __name__ == "__main__":
    start_program()
