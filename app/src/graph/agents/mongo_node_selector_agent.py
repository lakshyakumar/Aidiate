import os
from pydantic_ai import Agent
from app.src.type.type import CrudOperation

query_selector_agent = Agent(
    os.getenv("MODEL"),
    output_type=CrudOperation,
    system_prompt=(
        'You are an agent that can depend on queries provide an enum value describing the operation in query'
    )
)