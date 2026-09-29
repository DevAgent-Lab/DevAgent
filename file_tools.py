from multiprocessing.forkserver import read_signed
from pathlib import Path

WORKSPACE = Path("./workspace").resolve()

def resolve_workspace_path(file_path: str) -> Path:
    path = (WORKSPACE / file_path).resolve()

    if WORKSPACE not in path.parents and path != WORKSPACE:
        raise ValueError("Access outside workspace is not allowed.")

    return path

def list_files() -> list[str]:
     if not WORKSPACE.exists():
         return []

     return [
         str(path.relative_to(WORKSPACE))
         for path in WORKSPACE.rglob("*")
         if path.is_file()
     ]

def read_file(file_path: str) -> str:
    path = resolve_workspace_path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if not path.is_file():
        raise ValueError(f"Not a file: {file_path}")

    return path.read_text(encoding="utf-8")

def write_file(file_path: str, content: str) -> None:
    path = resolve_workspace_path(file_path)

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")

if __name__ == "__main__":
    print("=== FILES ===")
    print(list_files())

    print("\n=== READ ===")
    print(read_file("hello.txt"))

    print("\n=== WRITE ===")
    write_file("generated/example.txt", "Hello from DevAgent")
    print(read_file("generated/example.txt"))

if __name__ == "__main__":
    print(read_file("hello.txt"))

    try:
        read_file("../secret.txt")
    except ValueError as e:
        print("BLOCKED:", e)