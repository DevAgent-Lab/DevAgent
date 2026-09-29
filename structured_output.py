from dotenv import load_dotenv
from pydantic import BaseModel
from openai import OpenAI

load_dotenv()
client = OpenAI()

class Feature(BaseModel):
    name: str
    description: str

class DataField(BaseModel):
    name: str
    type: str
    description: str

class Requirement(BaseModel):
    project_type: str
    description: str

    core_features: list[Feature]
    constraints: list[str]
    data_fields: list[DataField]
    interfaces: list[str]

response = client.responses.parse(
    model="gpt-5.6-luna",
    instructions="""
    You are the Requirement Analysis step of DevAgent.
    Convert the user's request into structured software requirements.
    
    Rules:
    - Extract requirements primarily from what the user actually requested.
    - Do not decide implementation details unless explicitly requested.
    - Do not choose libraries, database technologies, package structures, or validation frameworks.
    - Do not invent arbitrary limits such as maximum string lengths.
    - Do not add features that the user did not request.
    - Keep implementation decisions for the later Planning step.
    """,
    input="""
    하루에 한 번 일기를 작성 할 수 있는 Spring Boot Rest API를 만들어줘.
    일기는 작성과 조회가 가능하고 하루에 하나만 작성 할 수 있어.
    """,
    text_format=Requirement,
)

requirement = response.output_parsed

class Task(BaseModel):
    id: int
    name: str
    description: str

class ProjectPlan(BaseModel):
    tech_stack: list[str]
    project_structure: list[str]
    dependencies: list[str]
    tasks: list[Task]

plan_response = client.responses.parse(
    model="gpt-5.6-luna",
    instructions="""
    You are the Planning step of DevAgent.
    Create an implementation plan from the given requirements.
    
    You may now decide
    - technical stack
    - dependencies
    - project structures
    - implementation tasks
    
    Current DevAgent v0.1 supported stack:
    - Java
    - Spring Boot
    - Gradle
    - Spring Web
    - Spring Data JPA
    - H2
    - JUnit
    - REST API
    
    Rules:
    - Stay within the currently supported stack.
    - Use Gradle, not Maven.
    - Keep the plan simple and appropriate for an MVP.
    """,
    input=requirement.model_dump_json(),
    text_format=ProjectPlan,
)

plan = plan_response.output_parsed

print("\n=== REQUIREMENT ===")
print(requirement.model_dump_json(indent=2))

print("\n=== PROJECT PLAN ===")
print(plan.model_dump_json(indent=2))