from openai import OpenAI

from devagent.models.requirement import Requirement
from devagent.prompts.requirement import REQUIREMENT_SYSTEM_PROMPT


client = OpenAI()

def create_requirement(user_prompt: str) -> Requirement:
    response = client.responses.parse(
        model = "gpt-5.6-luna",
        instructions = REQUIREMENT_SYSTEM_PROMPT,
        input = user_prompt,
        text_format = Requirement,
    )
    return response.output_parsed