from http.client import NO_CONTENT, HTTPResponse
from fastapi import APIRouter, Body, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response
from models import EntryModel, UpdateEntryModel

router = APIRouter()

@router.get("/", response_description="Test call")
async def get():
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.get("/api/", response_description="List all entries")
async def get_entries(request: Request):
    entries_first = []
    docs = request.app.mongodb["Entries"].find()
    for doc in await request.app.mongodb["Entries"].find().to_list(length=10000):
        entries_first.append(doc)
    entries = sorted(entries_first, key=lambda x: x['night'])
    entries.reverse()
    return entries


@router.get("/api/{id}", response_description="Get one particular entry")
async def get_one_entry(id: str, request: Request):
    entry = await request.app.mongodb["Entries"].find_one({"_id": id})
    return entry

@router.post("/api/", response_description="Log a new entry")
async def post_entry(request: Request, entry: EntryModel = Body(...)):
    entry = jsonable_encoder(entry)
    isNightSame = await request.app.mongodb["Entries"].find_one({"night": entry["night"]})
    if not isNightSame:
        new_entry = await request.app.mongodb["Entries"].insert_one(entry)
        created_entry = await request.app.mongodb["Entries"].find_one(
            {"_id": new_entry.inserted_id}
        )
    else:
        created_entry=entry

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_entry)


@router.put("/api/{id}", response_description="Update an existing entry")
async def put_entry(id: str, request: Request, entry: UpdateEntryModel = Body(...)):
    entry = {k: v for k, v in entry.dict().items() if v is not None}
    if len(entry) >= 1:
        update_result = await request.app.mongodb["Entries"].update_one(
            {"_id": id}, {"$set": entry}
        )
    if update_result.modified_count == 1:
        if (
            updated_entry := await request.app.mongodb["Entries"].find_one({"_id": id})
        ) is not None:
            return updated_entry
    if (
        existing_entry := await request.app.mongodb["Entries"].find_one({"_id": id})
    ) is not None:
        return existing_entry

    raise HTTPException(status_code=404, detail=f"Task {id} not found")


@router.delete("/api/{id}", response_description="Delete an unwanted entry")
async def delete_entry(id: str, request: Request, response: Response):
    delete_result = await request.app.mongodb["Entries"].delete_one({"_id": id})
    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
