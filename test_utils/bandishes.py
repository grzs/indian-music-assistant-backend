import os
import json

from typing import List
from pydantic import BaseModel

from app import app


def slurp_bandish_files(folder):
    bandishes = []
    for fname in filter(lambda f: f.endswith(".json"), os.listdir(folder)):
        try:
            fpath = os.path.join(folder, fname)
            with open(fpath) as freader:
                data = json.load(freader)
            bandishes.append({"name": fname[: len(".json") * -1], "lines": data})
        except FileNotFoundError as e:
            print(e)

    return bandishes


BANDISHES = slurp_bandish_files(folder="test_data")


class Bandish(BaseModel):
    name: str = None
    # taal: str = None
    # raag: str = None
    lines: List[List[List]] = []


# test endpoints
@app.post("/api/test/bandish")
def create_bandish(data: Bandish):
    BANDISHES.append(data)
    return data


@app.get("/api/test/bandishes", response_model=list[Bandish])
def list_bandishes(limit: int = 10):
    return BANDISHES[0:limit]


@app.get("/api/test/bandishes/{bandish_id}", response_model=Bandish)
def get_bandish(bandish_id: int) -> Bandish:
    bandish = BANDISHES[bandish_id]
    return bandish
