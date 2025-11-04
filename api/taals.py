from typing import List
from pydantic import BaseModel
from fastapi import HTTPException

from app import app


class Anga(BaseModel):
    is_tali: bool = True
    bols: List[str] = []


class Taal(BaseModel):
    slug: str = ""
    display_name: str = None
    angas: List[Anga] = []


## mongodb CRUD endpoints
@app.post("/api/v1/taal", response_model=Taal)
async def create_taal(taal: Taal):
    result = await app.mongodb["taals"].insert_one(taal.dict())
    inserted_taal = await app.mongodb["taals"].find_one({"_id": result.inserted_id})
    return inserted_taal


@app.get("/api/v1/taals", response_model=List[Taal])
async def read_taals():
    taals = await app.mongodb["taals"].find().to_list(None)
    return taals


@app.get("/api/v1/taals/{slug}", response_model=Taal)
async def read_taal_by_slug(slug: str):
    taal = await app.mongodb["taals"].find_one({"slug": slug})
    if taal is None:
        raise HTTPException(status_code=404, detail="Taal not found")
    return taal


@app.put("/api/v1/taals/{slug}", response_model=Taal)
async def update_taal(slug: str, taal: Taal):
    updated_result = await app.mongodb["taals"].update_one(
        {"slug": slug}, {"$set": taal.dict(exclude_unset=True)}
    )
    if updated_result.modified_count == 0:
        raise HTTPException(
            status_code=404, detail="Taal not found or no update needed"
        )
    updated_taal = await app.mongodb["taals"].find_one({"slug": slug})
    return updated_taal


@app.delete("/api/v1/taals/{slug}", response_model=dict)
async def delete_taal_by_slug(slug: str):
    delete_result = await app.mongodb["taals"].delete_one({"slug": slug})
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Taal not found")
    return {"message": "Taal deleted successfully"}
