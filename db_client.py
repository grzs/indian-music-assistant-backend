import json

from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from contextlib import asynccontextmanager


with open("db-credentials.json") as f:
    CREDENTIALS = json.load(f)


def get_connection_string(user, password, address, app_name):
    return f"mongodb+srv://{user}:{password}@{address}/?appName={app_name}"


# define a lifespan method for fastapi
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start the database connection
    await startup_db_client(app)
    yield
    # Close the database connection
    await shutdown_db_client(app)


# method for start the MongoDb Connection
async def startup_db_client(app):
    app.mongodb_client = AsyncIOMotorClient(get_connection_string(**CREDENTIALS))
    app.mongodb = app.mongodb_client.get_database("imt")
    print("MongoDB connected.")


# method to close the database connection
async def shutdown_db_client(app):
    app.mongodb_client.close()
    print("Database disconnected.")
