from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from dataclasses import dataclass

from app.src.utils.crud import MongoCRUD

@dataclass
class RouletteWheelGuessDeps:
    wheel_outcome: int
    
@dataclass
class EmailDependency:
    """
    Email object to be used in the agent
    """
    email: str
    crud: MongoCRUD
    
class MongoState(TypedDict):
    """
    State object to be used in the agent
    """
    email: str
    ideas: list
    crud: MongoCRUD
    query: str
    query_type: str
    messages: Annotated[list, add_messages]

# Define our state
class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    messages: Annotated[list, add_messages]
    roulette_number: int
    query: str
    won: bool