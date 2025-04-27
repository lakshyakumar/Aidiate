from ...types.common import State, RouletteWheelGuessDeps
from ..agents.agent import roulette_agent
from langchain_core.messages import  AIMessage, HumanMessage
import random

def first_node(state: State):
    roulette_number = random.randint(1, 20)
    return {"messages": [HumanMessage(content="From first_node")], "roulette_number": roulette_number}

def second_node(state: State):
    result = roulette_agent.run_sync(state["query"], deps=RouletteWheelGuessDeps( wheel_outcome=state["roulette_number"]))
    # Invoke the model
    return {"messages": [AIMessage(content="User has won" if result.output else "User has lost")], "won": result.output}