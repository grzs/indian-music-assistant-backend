import asyncio
import json
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi


async def ping_server(user, password, address, app_name):
    uri = f"mongodb+srv://{user}:{password}@{address}/?appName={app_name}&tls=true"

    # Set the Stable API version when creating a new client
    client = AsyncIOMotorClient(uri, server_api=ServerApi("1"))

    # Send a ping to confirm a successful connection
    try:
        await client.admin.command("ping")
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    with open(".db-credentials.json") as f:
        credentials = json.load(f)

    asyncio.run(ping_server(**credentials))
