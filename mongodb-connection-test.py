from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

import json


def ping_server(user, password, address, app_name):
    uri = f"mongodb+srv://{user}:{password}@{address}/?appName={app_name}"

    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi("1"))

    # Send a ping to confirm a successful connection
    try:
        client.admin.command("ping")
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    with open("db-credentials.json") as f:
        credentials = json.load(f)

    ping_server(app_name="IMT0", **credentials)
