from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class ConversationRecord:
    question: str
    answer: str

    model: str
    instructions: str
    context: str
    prompt: str

    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    cost: float

    search_time: float
    llm_time: float
    total_time: float
    id: int | None = None
    timestamp: datetime = field(default_factory=datetime.now)

def calculate_cost(model, usage):

    if "gpt-5-mini" in model:

        input_cost = (
            usage.input_tokens
            * 0.25
            / 1_000_000
        )

        output_cost = (
            usage.output_tokens
            * 2.00
            / 1_000_000
        )

        return input_cost + output_cost

    return 0.0
