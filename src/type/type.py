from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional
from ..utils.ai_utils import EmbeddingClass
from pydantic import BaseModel, EmailStr

class StageEnum(str, Enum):
    idea = "idea"
    prototype = "prototype"
    beta = "beta"
    launched = "launched"
    
class IdeaModelCRUDType(BaseModel):
    idea: str
    email: EmailStr
    tags: List[str]
    details: Optional[Dict[str, Any]] = None  # Use a dictionary for structured data


    class Config:
        from_attributes = True
        
    async def generate_vector(self):
        """
        Generating vector for the idea using OpenAI's embedding model.
        """
        openAIEmbed = EmbeddingClass()
        embedding = await openAIEmbed.embed(self.idea)
        return embedding
    
@dataclass
class IdeaModelWithScore:
    _id: str
    email: str
    idea: str
    tags: List[str]
    details: str
    stage: str
    score: float  # Add the score field
       
    
# Define a model for the update request
class IdeaUpdateModel(BaseModel):
    details: Optional[Dict[str, Any]] = None  # Use a dictionary for structured data
    stage: Optional[str] = None