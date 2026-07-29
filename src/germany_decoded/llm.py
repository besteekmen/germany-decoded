from dotenv import load_dotenv
from openai import OpenAI
from germany_decoded.prompt import INSTRUCTIONS, build_prompt
import time

load_dotenv()
client = OpenAI()

def ask_llm(question, context, model="gpt-5-mini"):
    prompt = build_prompt(question, context)

    input_messages = [
        {"role": "developer", "content": INSTRUCTIONS},
        {"role": "user", "content": prompt}
    ]

    t0 = time.time()
    response = client.responses.create(
        model=model,
        input=input_messages,
    )
    print("LLM:", time.time() - t0)

    return response.output_text