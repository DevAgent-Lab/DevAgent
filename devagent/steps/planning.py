from openai import OpenAI

from devagent.models.requirement import Requirement
from devagent.models.plan import ProjectPlan
from devagent.prompts.planning import PLANNING_SYSTEM_PROMPT

client = OpenAI()

def create_plan(requirement: Requirement) -> ProjectPlan:
    response = client.responses.parse(
        model="gpt-5.6-luna",
        instructions=PLANNING_SYSTEM_PROMPT,
        input=requirement.model_dump_json(indent=2),
        text_format=ProjectPlan,
    )

    return response.output_parsed