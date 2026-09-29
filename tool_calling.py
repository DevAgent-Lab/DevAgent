import json

from dotenv import load_dotenv
from openai import OpenAI

from file_tools import list_files, read_file, write_file
from shell_tools import run_command

load_dotenv()
client = OpenAI()

TOOLS = [
    {
        "type": "function",
        "name": "list_files",
        "description": "List all files inside the workspace.",
        "parameters" : {
            "type": "object",
            "properties": {},
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "read_file",
        "description": "Read a text file from the workspace.",
        "parameters" : {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path relative to the workspace.",
                }
            },
            "required": ["file_path"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "write_file",
        "description": "Write a text content to a file inside the workspace.",
        "parameters" : {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path relative to the workspace.",
                },
                "content": {
                    "type": "string",
                    "description": "Text content to write."
                }
            },
            "required": ["file_path", "content"],
            "additionalProperties": False,
        },
        "strict": True,
    },
    {
        "type": "function",
        "name": "run_command",
        "description": "Run a command inside the workspace.",
        "parameters": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Command and arguments.",
                }
            },
            "required": ["command"],
            "additionalProperties": False,
        },
        "strict": True,
    },
]

def execute_tool(name: str, arguments: dict):
    if name == "list_files":
        return list_files()

    if name == "read_file":
        return read_file(**arguments)

    if name == "write_file":
        write_file(**arguments)
        return {"success": True}

    if name == "run_command":
        result = run_command(**arguments)
        return result.model_dump()

    raise ValueError(f"Unknown tool: {name}")

response = client.responses.create(
    model="gpt-5.6-luna",
    input="""
    Create a Python file named hello.py in the workspace.
    
    The program must print exactly:
    Hello DevAgent
    
    After creating the file, run it and verify the output.
    Use the availavle tools.
    """,
    tools=TOOLS,
)

while True:
    tool_outputs =[]

    for item in response.output:
        if item.type != "function_call":
            continue

        arguments = json.loads(item.arguments)

        print(f"\nTool call: {item.name}")
        print(f"Argument: {arguments}")

        result = execute_tool(
            item.name,
            arguments,
        )

        print(f"Result: {result}")

        tool_outputs.append(
            {
                "type": "function_call_output",
                "call_id": item.call_id,
                "output": json.dumps(
                    result,
                    ensure_ascii=False,
                )
            }
        )

    if not tool_outputs:
        print("\n=== FINAL ===")
        print(response.output_text)
        break

    response = client.responses.create(
        model="gpt-5.6-luna",
        previous_response_id=response.id,
        input=tool_outputs,
        tools=TOOLS,
    )
