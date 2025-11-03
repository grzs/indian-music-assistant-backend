from fastapi import FastAPI
from pydantic import BaseModel

import os
import json


app = FastAPI()


class Matra(BaseModel):
    syllable: str = "-"
    sargam: str = "-"
    bol: str = "-"


class Bandish(BaseModel):
    name: str = None
    # taal: str = None
    # raag: str = None
    lines: list[list[list]] = []


bandishes = []


@app.get("/")
def root():
    return {"hello": "world"}


@app.post("/bandish")
def create_bandish(data: Bandish):
    bandishes.append(data)
    return data


@app.get("/bandishes", response_model=list[Bandish])
def list_bandishes(limit: int = 10):
    return bandishes[0:limit]


@app.get("/bandishes/{bandish_id}", response_model=Bandish)
def get_bandish(bandish_id: int) -> Bandish:
    bandish = bandishes[bandish_id]
    return bandish


def slurp_bandish_files(fs_root):
    for fname in filter(lambda f: f.endswith(".json"), os.listdir(fs_root)):
        try:
            fpath = os.path.join(fs_root, fname)
            with open(fpath) as freader:
                data = json.load(freader)
            bandishes.append({"name": fname[: len(".json") * -1], "lines": data})
        except FileNotFoundError:
            print("file not found")


slurp_bandish_files("data")
