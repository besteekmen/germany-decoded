import time
from dotenv import load_dotenv
from openai import OpenAI
from germany_decoded.retrieval import search_hybrid
from germany_decoded.metrics import ConversationRecord, calculate_cost
from germany_decoded.db.conversation import save_conversation

INSTRUCTIONS = """
You are Germany Decoded, an AI assistant that helps English speakers understand German law.

Rules:
- Answer in clear English.
- Base every answer ONLY on the provided legal context.
- Do not invent facts or legal information.
- Do not provide definitive legal advice or make legal decisions.
- Do not discuss legal rules that are not present in the provided context.
- If the context does not answer the question or is insufficient, clearly say so.
- Explain the law in plain English.
- Quote or summarize the law accurately without changing its meaning.
- Mention the relevant legal section(s).
- Include the official source URL(s).

Keep answers under 250 words unless the user explicitly asks for more detail.
Structure every answer as:

1. Short answer
2. Explanation
3. Relevant legal sections
4. Official sources
""".strip()

PROMPT_TEMPLATE = """
Question: {question}

Legal context:
{context}

Answer:
""".strip()

load_dotenv()
client = OpenAI()

class Assistant:
    def __init__(
        self,
        instructions=INSTRUCTIONS,
        prompt_template=PROMPT_TEMPLATE,
        model="gpt-5-mini",
    ):
        self.instructions = instructions
        self.prompt_template = prompt_template
        self.model = model
        self.last_call: ConversationRecord | None = None

    def ask(self, question):
        start_total = time.time()

        start_search = time.time()
        results = self.search(question)
        search_time = time.time() - start_search

        context = self.build_context(results)
        prompt = self.build_prompt(question, context)

        start_llm = time.time()
        response = self.llm(prompt)
        llm_time = time.time() - start_llm
        total_time = time.time() - start_total

        self._log_response(
            question=question,
            context=context,
            prompt=prompt,
            response=response,
            search_time=search_time,
            llm_time=llm_time,
            total_time=total_time
        )

        return {
            "answer": response.output_text,
            "sources": results,
            "conversation_id": self.last_call.id
        }

    def search(self, question, top_k=3):
        return search_hybrid(question, top_k=top_k)

    def build_context(self, results):
        """
        Build the context sent to the LLM.
        """

        parts = []

        for result in results:
            part = (
                f"[{result['law']} {result['section']}]\n"
                f"Title: {result['title']}\n\n"
                f"{result['content']}\n\n"
                f"Source: {result['source']}"
            )
            parts.append(part)

        return "\n\n--------------------\n\n".join(parts)

    def build_prompt(self, question, context):
        return self.prompt_template.format(
            question=question,
            context=context
        )

    def llm(self, prompt):
        input_messages = [
            {"role": "developer", "content": self.instructions},
            {"role": "user", "content": prompt}
        ]

        return client.responses.create(
            model=self.model,
            input=input_messages,
        )

    def _log_response(
        self,
        question,
        context,
        prompt,
        response,
        search_time,
        llm_time,
        total_time,
    ):
        usage = response.usage

        call_record = ConversationRecord(
            question=question,
            answer=response.output_text,
            model=self.model,
            instructions=self.instructions,
            context=context,
            prompt=prompt,
            prompt_tokens=usage.input_tokens,
            completion_tokens=usage.output_tokens,
            total_tokens=usage.total_tokens,
            cost=calculate_cost(self.model, usage),
            search_time=search_time,
            llm_time=llm_time,
            total_time=total_time,
        )
        conversation_id = save_conversation(call_record)
        call_record.id = conversation_id
        self.last_call = call_record
        