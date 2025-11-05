import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from db_client import lifespan

# creating a server with python FastAPI
app = FastAPI(lifespan=lifespan)

# CORS middleware config
origins = [
    "http://localhost:8080",
    os.environ.get("FRONTEND_URI", "http://localhost"),
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
