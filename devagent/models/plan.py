from pydantic import BaseModel, Field

class TechStack(BaseModel):
    language: str = Field(description="주 프로그래밍 언어")
    framework: str = Field(description="주요 프레임워크")
    build_tool: str = Field(description="빌드 도구")
    database: str = Field(description="데이터베이스")

class Dependency(BaseModel):
    name: str = Field(description="Dependency 이름")
    purpose: str = Field(description="Dependency 사용 목적")

class ProjectFile(BaseModel):
    path: str = Field(description="프로젝트 내 파일 또는 디렉토리 경로")
    purpose: str = Field(description="해당 파일 또는 디렉토리의 역할")

class Task(BaseModel):
    id: int = Field(description="Task 순번")
    name: str = Field(description="Task 이름")
    description: str = Field(description="Task에서 수행할 작업")

class ProjectPlan(BaseModel):
    tech_stack: TechStack
    
    assumptions: list[str] = Field(
        default_factory=list,
        description="요구사항에 명시되지 않았지만 구현을 위해 Planner가 둔 최소한의 가정"
    )

    dependencies: list[Dependency] = Field(
        default_factory=list,
        description="프로젝트에 필요한 주요 Dependency"
    )

    project_structure: list[ProjectFile] = Field(
        default_factory=list,
        description="생성해야할 주요 파일 및 디렉토리 구조"
    )

    tasks: list[Task] = Field(
        description="구현 작업의 실행 순서"
    )