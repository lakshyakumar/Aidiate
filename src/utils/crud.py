from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from typing import Type, TypeVar, Generic
from pydantic import BaseModel

from .ai_utils import EmbeddingClass

from ..types.types import IdeaModelWithScore, StageEnum

T = TypeVar("T", bound=BaseModel)

class MongoCRUD(Generic[T]):
    def __init__(self, db_url: str, db_name: str, collection_name: str, model: Type[T]):
        self.client = AsyncIOMotorClient(db_url)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]
        self.model = model
        self.openAIEmbed = EmbeddingClass()  # Assuming EmbeddingClass is defined elsewhere

    async def create(self, data: T) -> str:
        try:
            # Automatically add a default stage value
            data_dict = data.dict()
            data_dict["stage"] = StageEnum.idea  # Assuming StageEnum is defined elsewhere
            # Generate vector using the generate_vector method
            data_dict["vector"] = await data.generate_vector()
            result = await self.collection.insert_one(data_dict)
            return str(result.inserted_id)
        except Exception as e:
            print(f"Error in create: {e}")
            raise HTTPException(status_code=500, detail="Error creating data in database")

    async def read(self, query: dict = {}) -> list[T]:
        try:
            if "_id" in query and isinstance(query["_id"], str):
                query["_id"] = ObjectId(query["_id"])
            cursor = self.collection.find(query)
            results = []  
            async for doc in cursor:
                # Convert _id to string
                doc["_id"] = str(doc["_id"])
                results.append(self.model(**doc))
            return results
        except Exception as e:
            # Log the error (you can replace this with proper logging)
            print(f"Error in read: {e}")
            raise HTTPException(status_code=500, detail="Error reading data from database")

    async def update(self, id: str, data: dict) -> dict:
        try:
            # Check if id is valid and convert to ObjectId
            try:
                object_id = ObjectId(id)  # Ensure id is a valid ObjectId
            except Exception as e:
                raise HTTPException(status_code=400, detail="Invalid ObjectId format")

            # Perform the update operation
            result = await self.collection.update_one({"_id": object_id}, data)

            if result.matched_count == 0:
                raise HTTPException(status_code=404, detail="Item not found")

            # Fetch the updated document
            updated_document = await self.collection.find_one({"_id": object_id})
            if not updated_document:
                raise HTTPException(status_code=404, detail="Updated document not found")

            # Convert ObjectId to string for the response
            updated_document["_id"] = str(updated_document["_id"])

            return updated_document  # Return the updated document

        except Exception as e:
            print(f"Error in update: {e}")
            raise HTTPException(status_code=500, detail="Error updating data in database")

    async def delete(self, id_or_query: dict | str) -> dict:
        try:
            if isinstance(id_or_query, dict):
                id = id_or_query.get("_id")
            else:
                id = id_or_query

            await self.collection.delete_one({"_id": ObjectId(id)})
            return {"deleted": True}

        except Exception as e:
            print(f"Error in delete: {e}")
            raise HTTPException(status_code=500, detail="Error deleting data from database")
   
   
    async def find_similar_by_embedding(
        self,
        query: str,
        email: str,
        top_k: int = 1
    ) -> list[T]:
        try:
            query_embedding = await self.openAIEmbed.embed(query)
            pipeline = [
                {
                    "$vectorSearch": {
                        "index": "vector_index",  # 👈 your index name
                        "queryVector": query_embedding,
                        "path": "vector",
                        "filter": {
                                "email": email
                        },
                        "numCandidates": 100,
                        "limit": top_k,
                    }
                },
                {
                    "$addFields": {
                        "score": {"$meta": "vectorSearchScore"}
                    }
                },
                {
                    "$project": {
                        "vector": 1,  # Exclude the vector field from the result
                        "email": 1,  # Exclude the email field from the result
                        "idea": 1,
                        "tags": 1,
                        "details": 1,
                        "stage": 1,
                        "_id": 1,
                        "score": 1 
                    }
                }
            ]

            cursor = self.collection.aggregate(pipeline)
            results = []
            async for doc in cursor:
                doc["_id"] = str(doc["_id"])
                result = IdeaModelWithScore(
                    _id=doc["_id"],
                    email=doc["email"],
                    idea=doc["idea"],
                    tags=doc["tags"],
                    details=doc["details"],
                    stage=doc["stage"],
                    score=doc["score"]  # Include the score
                )
                results.append(result)
            results = [res for res in results if res.score > 0.9]  # Filter results by email
            return results

        except Exception as e:
            print(f"Error in find_similar_by_embedding: {e}")
            raise HTTPException(status_code=500, detail="Error finding similar embeddings")
           