import os

from ..agents.mongo_agent import mongo_agent
from ...models.idea_db_model import IdeaModel
from ...utils.crud import MongoCRUD
from ...type.common import MongoState, EmailDependency
from langchain_core.messages import  AIMessage, HumanMessage


def init_node(state: MongoState):
    db_url = os.getenv("MONGO_URI")

    if not db_url:
        raise ValueError("DB_URL environment variable not set.")
    
    crud = MongoCRUD(
        db_url=db_url,
        db_name="aidiate",
        collection_name="ideas",
        model=IdeaModel
    )

    return {"messages": [HumanMessage(content="From first_node")], "email": "user@example.com", "crud": crud, "ideas": []}


def mongo_node(state: MongoState):
    result = mongo_agent.run_sync(state["query"], deps=EmailDependency( email=state["email"], crud=state["crud"]))
    # Invoke the model
    return {"messages": [AIMessage(content=result.output)], "ideas": result, "email": state["email"], "crud": state["crud"]}