from fastapi import APIRouter , Query
from app.src.graph.graph import GraphBuilder

# Create a router instance
router = APIRouter()

mongo_graph = GraphBuilder()
mongo_graph.compile()

# Define the /aidiate route
@router.get("/")
def aidiate(query: str = Query(..., description="What is your aidiate query?")):
    result = mongo_graph.invoke_graph(query)
    return {"message": result["messages"][-1].content}