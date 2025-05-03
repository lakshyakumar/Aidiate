import os

from ..agents.mongo_agent import mongo_get_agent, mongo_create_agent
from ..agents.mongo_node_selector_agent import query_selector_agent
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


def mongo_get_node(state: MongoState):
    result = mongo_get_agent.run_sync(state["query"], deps=EmailDependency( email=state["email"], crud=state["crud"]))
    # Invoke the model
    return {"messages": [AIMessage(content=result.output)], "ideas": result, "email": state["email"], "crud": state["crud"]}

def mongo_create_node(state: MongoState):
    result = mongo_create_agent.run_sync(state["query"], deps=EmailDependency( email=state["email"], crud=state["crud"]))
    # Invoke the model
    return {"messages": [AIMessage(content=result.output)], "ideas": result, "email": state["email"], "crud": state["crud"]}


def mongo_query_node_selector(state: MongoState):
    result = query_selector_agent.run_sync(state["query"])
    # Invoke the model
    # return {"messages": [AIMessage(content=result)], "query_type": result}
    return {"messages": [AIMessage(content=result.output)], "query_type": result.output}