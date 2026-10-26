from dotenv import load_dotenv

load_dotenv()

from devagent.steps.requirement import create_requirement
from devagent.steps.planning import create_plan


def main():
    user_prompt = input("무엇을 만들고 싶나요?\n> ")

    requirement = create_requirement(user_prompt)

    print("\n=== Requirement ===")
    print(requirement.model_dump_json(indent=2))

    plan = create_plan(requirement)

    print("\n=== Project Plan ===")
    print(plan.model_dump_json(indent=2))

if __name__ == "__main__":
    main()