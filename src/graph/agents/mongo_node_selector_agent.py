from pydantic_ai import Agent, RunContext
from typing import Any, Dict, List, Optional

from ...type.type import IdeaModelCRUDType, CrudOperation
from ...type.common import EmailDependency
import os



query_selector_agent = Agent(
    os.getenv("MODEL"),
    output_type=CrudOperation,
    system_prompt=(
        'You are an agent that can depend on queries provide an enum value describing the operation in query'
    )
)