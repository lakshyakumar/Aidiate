from pydantic_ai import Agent, RunContext
from typing import Any, Dict, List, Optional

from app.src.type.type import IdeaModelCRUDType
from app.src.type.common import EmailDependency
import os


mongo_get_agent = Agent(  
    os.getenv("MODEL"),
    deps_type=EmailDependency,
    output_type=str,
    system_prompt=(
        'You are an agent that can manage user ideas with MongoDB database Get all and find operations based on Email.'
        'Your task is to respond with the appropriate tool results for the users get queries.'
        'Use the `get_ideas` function to retrieve ideas associated with the provided email this dont require any title, it gets all ideas.' 
        'In case you have idea or context about title use `find_ideas`'
        'Use the `find_ideas` function to find similar ideas based on the provided query. This can match teh indexed ideas in the database.'
    ),
)


mongo_create_agent = Agent(  
    os.getenv("MODEL"),
    deps_type=EmailDependency,
    output_type=str,
    system_prompt=(
        'You are an agent that can manage user ideas with MongoDB database CRUD operations based on Email.'
        'Your task is to respond with the appropriate tool results for the users queries.'
        'Use the `get_ideas` function to retrieve ideas associated with the provided email this dont require any title, it gets all ideas. I case you ahve idea or context about title use `find_ideas`'
        'Use the `add_ideas` function to add or create ideas in the database. Dynamically create a idea name, details and tags, without asking user for it'
        'For creating idea details, create it ion the format of a dictionary with the following keys: "description",  "priority", "market trends", "Growth", "products" and so on try to fill it by yourself.'
        'Use the `find_ideas` function to find similar ideas based on the provided query. This can match teh indexed ideas in the database.'
    ),
)



@mongo_get_agent.tool
async def get_ideas(ctx: RunContext[EmailDependency]) -> Optional[List[Any]]:
    """
    Fetch ideas from MongoDB based on the provided email.
    """
    result = await ctx.deps.crud.read({"email": ctx.deps.email})
    return result

@mongo_create_agent.tool
async def add_ideas(ctx: RunContext[EmailDependency], idea: str, tags: List[str], details: Optional[Dict[str, Any]]) -> Optional[List[Any]]:
    """
    Adds or creates ideas to MongoDB based on the provided email information.
    """
    data = {
        "idea": idea,
        "email": ctx.deps.email,
        "tags": tags,
        "details": details,
    }
    idea_model = IdeaModelCRUDType(**data)
    result = await ctx.deps.crud.create(idea_model)
    return result

@mongo_get_agent.tool
async def find_ideas(ctx: RunContext[EmailDependency], query: str) -> Optional[List[Any]]:
    """
    Find ideas in MongoDB based on the provided query.
    """
    result = await ctx.deps.crud.find_similar_by_embedding(query, ctx.deps.email,5)
    return result