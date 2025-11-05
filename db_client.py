import os
import json

from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from contextlib import asynccontextmanager


def get_connection_string():
    creds_file = os.environ.get("DB_CREDENTIALS_JSON", ".db-credentials.json")

    with open(creds_file) as f:
        credentials = json.load(f)

    return "mongodb+srv://{user}:{password}@{address}/?appName={app_name}".format(
        **credentials
    )


async def startup_db_client(app):
    app.mongodb_client = AsyncIOMotorClient(get_connection_string())
    app.mongodb = app.mongodb_client.get_database("imt")
    print("MongoDB connected.")


async def shutdown_db_client(app):
    app.mongodb_client.close()
    print("Database disconnected.")


# define a lifespan method for fastapi
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start the database connection
    await startup_db_client(app)
    yield
    # Close the database connection
    await shutdown_db_client(app)
