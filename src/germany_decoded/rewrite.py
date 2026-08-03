import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

def extract_legal_concept(question: str) -> str:
    """
    Extract the single legal concept that best represents the user's question
    for PostgreSQL Full Text Search.
    """

    response = client.responses.create(
        model="gpt-5-mini",
        input=[
            {
                "role": "system",
                "content": (
                    "You are helping search the German Civil Code (BGB).\n\n"

                    "The user's question may contain several ideas.\n"
                    "Return ONLY the single most important German legal concept "
                    "that should be searched.\n\n"

                    "Rules:\n"
                    "- Return exactly ONE German legal concept.\n"
                    "- Prefer official BGB terminology.\n"
                    "- Maximum 3 words.\n"
                    "- Use a noun or noun phrase.\n"
                    "- Do NOT write a sentence.\n"
                    "- Do NOT explain anything.\n"
                    "- Do NOT answer the question.\n"
                    "- Output only the legal concept.\n\n"

                    "Examples:\n"
                    "Can my landlord keep my deposit?\n"
                    "-> Mietsicherheit\n\n"

                    "Can I reduce my rent because of mold?\n"
                    "-> Mietminderung\n\n"

                    "Who pays for normal wear and tear?\n"
                    "-> vertragsgemäßer Gebrauch\n\n"

                    "Who repairs defects?\n"
                    "-> Erhaltungspflicht\n\n"

                    "Can my landlord terminate immediately?\n"
                    "-> fristlose Kündigung"
                ),
            },
            {
                "role": "user",
                "content": question,
            },
        ],
    )

    return response.output_text.strip()