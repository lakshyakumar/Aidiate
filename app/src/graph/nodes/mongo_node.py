"""
This module provides functionality for initializing and interacting with MongoDB nodes 
using various agents and utilities. It includes methods for initializing a node, 
retrieving data, creating data, and selecting query types.
"""
import os

from langchain_core.messages import  AIMessage, HumanMessage

from app.src.graph.agents.mongo_agent import mongo_get_agent, mongo_create_agent
from app.src.graph.agents.mongo_node_selector_agent import query_selector_agent
from app.src.models.idea_db_model import IdeaModel
from app.src.type.common import MongoState, EmailDependency
from app.src.utils.crud import MongoCRUD

def init_node():
    """
    Initialize the node with a MongoDB connection and set up the initial state.
    Parameters:
        Note: (This function no longer takes a state parameter.)
    Returns:
        - dict: The initial state of the node with messages, email, CRUD operations, and ideas.
    """
    db_url = os.getenv("MONGO_URI")

    if not db_url:
        raise ValueError("DB_URL environment variable not set.")

    crud = MongoCRUD(
        db_url=db_url,
        db_name="aidiate",
        collection_name="ideas",
        model=IdeaModel
    )

    return {
        "messages": [HumanMessage(content="From first_node")], 
        "email": "user@example.com", "crud": crud, "ideas": []
        }

def mongo_get_node(state: MongoState):
    """
    Retrieve data from the MongoDB database using the provided query.
    Parameters:
        - state (MongoState): The current state of the node.
    Returns:
        - dict: The result of the query, including messages, email, CRUD operations, and ideas.
    """
    result = mongo_get_agent.run_sync(state["query"], 
                                      deps=EmailDependency(email=state["email"], crud=state["crud"]))

    # Invoke the model
    return {"messages": [AIMessage(content=result.output)], 
            "ideas": result, 
            "email": state["email"], 
            "crud": state["crud"]
            }

def mongo_create_node(state: MongoState):
    """
    Create data in the MongoDB database using the provided query.
    Parameters:
        - state (MongoState): The current state of the node.
    Returns:
        - dict: The result of the creation, including messages, email, CRUD operations, and ideas.
    """
    result = mongo_create_agent.run_sync(state["query"], 
                                         deps=EmailDependency( email=state["email"], crud=state["crud"]))
    # Invoke the model
    return {"messages": [AIMessage(content=result.output)], "ideas": result, "email": state["email"], "crud": state["crud"]}


def mongo_query_node_selector(state: MongoState):
    """
    Select a query type based on the provided query.
    Parameters:
        - state (MongoState): The current state of the node.
    Returns:
        - dict: The result of the query selection, including messages and query type.
    """
    result = query_selector_agent.run_sync(state["query"])
    # Invoke the model
    # return {"messages": [AIMessage(content=result)], "query_type": result}
    return {"messages": [AIMessage(content=result.output)], "query_type": result.output}