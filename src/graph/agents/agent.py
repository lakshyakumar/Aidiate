
from pydantic_ai import Agent, RunContext
from ...types.common import RouletteWheelGuessDeps
import os


roulette_agent = Agent(  
    os.getenv("MODEL"),
    deps_type=RouletteWheelGuessDeps,
    output_type=bool,
    system_prompt=(
        'Use the `roulette_wheel` function to see if the '
        'customer has won based on the number they provide.'
    ),
)

@roulette_agent.tool
def get_tasks(ctx: RunContext[RouletteWheelGuessDeps], guessed: int) -> str:
    """
    Match the user's guess with roulette wheel outcome
    """
    return 'winner' if guessed == ctx.deps.wheel_outcome else 'loser'