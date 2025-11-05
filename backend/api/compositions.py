from typing import List
from pydantic import BaseModel
from fastapi import HTTPException

from app import app


class Matra(BaseModel):
    syllable: str = "-"
    sargam: str = "-"
    bol: str = "-"


class Line(BaseModel):
    section: str = "-"
    matras: List[Matra] = []


class Composition(BaseModel):
    slug: str = ""
    type: str = ""  # taal, gat or bandish
    display_name: str = None
    raag: str = None
    taal: str = None
    lines: List[Line] = []


## mongodb CRUD endpoints
@app.post("/api/v1/composition", response_model=Composition)
async def create_composition(composition: Composition):
    result = await app.mongodb["compositions"].insert_one(composition.dict())
    inserted_composition = await app.mongodb["compositions"].find_one(
        {"_id": result.inserted_id}
    )
    return inserted_composition


@app.get("/api/v1/compositions", response_model=List[Composition])
async def read_compositions():
    compositions = await app.mongodb["compositions"].find().to_list(None)
    return compositions


@app.get("/api/v1/compositions/{slug}", response_model=Composition)
async def read_composition_by_slug(slug: str):
    composition = await app.mongodb["compositions"].find_one({"slug": slug})
    if composition is None:
        raise HTTPException(status_code=404, detail="Composition not found")
    return composition


@app.put("/api/v1/compositions/{slug}", response_model=Composition)
async def update_composition(slug: str, composition: Composition):
    updated_result = await app.mongodb["compositions"].update_one(
        {"slug": slug}, {"$set": composition.dict(exclude_unset=True)}
    )
    if updated_result.modified_count == 0:
        raise HTTPException(
            status_code=404, detail="Composition not found or no update needed"
        )
    updated_composition = await app.mongodb["compositions"].find_one({"slug": slug})
    return updated_composition


@app.delete("/api/v1/compositions/{slug}", response_model=dict)
async def delete_composition_by_slug(slug: str):
    delete_result = await app.mongodb["compositions"].delete_one({"slug": slug})
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Composition not found")
    return {"message": "Composition deleted successfully"}
