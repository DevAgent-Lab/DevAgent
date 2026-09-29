import subprocess
from pydantic import BaseModel
from file_tools import WORKSPACE

class CommandResult(BaseModel):
    command: list[str]
    exit_code: int
    stdout: str
    stderr: str

def run_command(command: list[str], timeout: int=30) -> CommandResult:
    try:
        result = subprocess.run(
            command,
            cwd=WORKSPACE,
            capture_output=True,
            text=True,
            timeout=timeout,
            shell=False,
        )

        return CommandResult(
            command=command,
            exit_code=result.returncode,
            stdout=result.stdout,
            stderr=result.stderr,
        )
    except subprocess.TimeoutExpired as e:
        return CommandResult(
            command=command,
            exit_code=-1,
            stdout=e.stdout or "",
            stderr=f"Command timed out after {timeout} seconds.",
        )

if __name__ == "__main__":
    result = run_command(
        ["python", "-c", "print('Hello from Shell Tool')"]
    )

    print(result.model_dump_json(indent=2))

if __name__ == "__main__":
    success = run_command(
        ["python", "-c", "print('Hello from Shell Tool')"]
    )

    print("=== SUCCESS ===")
    print(success.model_dump_json(indent=2))

    failure = run_command(
        ["python", "-c", "raise Exception('Test Error')"]
    )

    print("\n=== FAILURE ===")
    print(failure.model_dump_json(indent=2))