from devagent.steps.requirement import create_requirement

def main():
    user_prompt = input("무엇을 만들고 싶나요?\n> ")

    requirement = create_requirement(user_prompt)

    print("\n=== Requirement ===")
    print(requirement.model_dump_json(indent=2))

if __name__ == "__main__":
    main()