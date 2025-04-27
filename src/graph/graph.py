from ..types.common import MongoState
from .nodes.mongo_node import init_node, mongo_node
from langgraph.graph import END, START, StateGraph
from langchain_core.messages import  AIMessage, HumanMessage

class GraphBuilder:
    compiled_graph = None
    def __init__(self):
        # Initialize the StateGraph with the State class
        self.graph_builder = StateGraph(MongoState)

        # Add all the nodes
        self.graph_builder.add_node("init_node", init_node)
        self.graph_builder.add_node("mongo_node", mongo_node)

        # Add the edges
        self.graph_builder.add_edge(START, "init_node")
        self.graph_builder.add_edge("init_node", "mongo_node")
        self.graph_builder.add_edge("mongo_node", END)

    def compile(self):
        """
        Compile the graph and return the compiled graph.
        """
        self.compiled_graph =  self.graph_builder.compile()

    def invoke_graph(self, query):
        """
        Take a query and create initial parameters for the graph.
        """
        if not self.compiled_graph:
            raise ValueError("Graph has not been compiled. Please call `compile` before invoking.")

        # Example of creating initial parameters based on the query
        initial_state = {"messages": [HumanMessage(content=query)], "query": query, "ideas": []}

        # Invoke the compiled graph with the initial state
        return self.compiled_graph.invoke(initial_state)