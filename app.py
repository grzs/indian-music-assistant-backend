from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from db_client import lifespan

# creating a server with python FastAPI
app = FastAPI(lifespan=lifespan)

# CORS middleware config
origins = [
    "http://localhost",
    "http://localhost:8080",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
