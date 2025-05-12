import os
from fastapi import APIRouter , Query
from fastapi import FastAPI, HTTPException, Query,  Depends
from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID

from app.src.type.type import IdeaModelCRUDType, IdeaUpdateModel
from app.src.utils.crud import MongoCRUD
from app.src.models.idea_db_model import IdeaModel
from bson import ObjectId

db_url = os.getenv("MONGO_URI")

if not db_url:
    raise ValueError("DB_URL environment variable not set.")

# Create a router instance
router = APIRouter()
crud = MongoCRUD(
    db_url=db_url,
    db_name="aidiate",
    collection_name="ideas",
    model=IdeaModel
)

# Define the /aidiate routes
@router.get("/", response_model=List[IdeaModel], summary="Get all ideas with optional filters")
async def get_ideas(
    email: Optional[str] = Query(None, description="Filter ideas by email"),
    stage: Optional[str] = Query(None, description="Filter ideas by stage"),
    tags: Optional[List[str]] = Query(None, description="Filter ideas by tags"),
):
    """
    Get all ideas with optional filters such as:
    - `email`: Filter by email.
    - `stage`: Filter by the stage of the idea.
    - `tags`: Filter by tags (match all provided tags).
    """
    query = {}
    if email:
        query["email"] = email
    else:
        raise HTTPException(status_code=400, detail=str("email is required"))
    if stage:
        query["stage"] = stage
    if tags:
        query["tags"] = {"$all": tags}  # Match all provided tags

    try:
        ideas = await crud.read(query)
        return ideas
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", response_model=IdeaModelCRUDType, summary="Create a new idea")
async def create_idea(idea: IdeaModelCRUDType):
    """
    Create a new idea in the database. 
    The response will contain the ID of the newly created idea.
    """
    try:
        idea_id = await crud.create(idea)
        # Return the created idea with MongoDB generated _id
        return {**idea.model_dump(), "_id": idea_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Define the endpoint to update an idea by ID
@router.put("/{idea_id}", response_model=IdeaModel, summary="Update an idea by ID")
async def update_idea(idea_id: str, update_data: IdeaUpdateModel):
    """
    Update an idea's details and/or stage by its ID.
    """
    try:
        # Find the idea by ID
        idea = await crud.read({"_id": idea_id})
        if not idea:
            raise HTTPException(status_code=404, detail="Idea not found")

        # Prepare the update fields
        update_fields = {}
        if update_data.details is not None:
            update_fields["details"] = update_data.details
        if update_data.stage is not None:
            update_fields["stage"] = update_data.stage

        # If no fields to update, raise an error
        if not update_fields:
            raise HTTPException(status_code=400, detail="No fields to update")

        # Update the idea
        updated_idea = await crud.update(
             idea_id,
            {"$set": update_fields}
        )

        return updated_idea
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

# Define the endpoint to delete an idea by ID
@router.delete("/{idea_id}", summary="Delete an idea by ID")
async def delete_idea(idea_id: str):
    """
    Delete an idea by its ID.
    """
    try:
        # Find the idea by ID
        idea = await crud.read({"_id": idea_id})
        if not idea:
            raise HTTPException(status_code=404, detail="Idea not found")

        # Delete the idea
        delete_result = await crud.delete({"_id": idea_id})
        if delete_result.deleted_count == 0:
            raise HTTPException(status_code=500, detail="Failed to delete the idea")

        return {"message": "Idea deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    
    
@router.post("/vector-search")
async def vector_search(
    query: str,
    email: str = Query(...),
    top_k: int = Query(5)
):
    try:
        results = await crud.find_similar_by_embedding(
            query=query,
            email=email,
            top_k=top_k
        )
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    