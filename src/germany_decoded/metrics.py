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
    #cost = 0
    #if "gpt-5-mini" in model:
        #cost = (usage.input_tokens * 0.15 + usage.output_tokens * 0.60) / 1_000_000
    return 0.0
