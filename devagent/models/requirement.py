from pydantic import BaseModel, Field

class Feature(BaseModel):
    name: str = Field(description="기능 이름")
    description: str = Field(description="기능에 대한 설명")

class DataRequirement(BaseModel):
    name: str = Field(description="필요한 데이터 이름")
    description: str = Field(description="데이터에 대한 설명")

class Requirement(BaseModel):
    project_name: str = Field(description="프로젝트 이름")
    project_type: str = Field(description="프로젝트 유형 ex) backend_api")
    summary: str = Field(description="사용자가 만들고자 하는 프로젝트의 핵심 목적")
    core_features: list[Feature] = Field(description="사용자가 요구했거나 프로젝트 목적상 반드시 필요한 핵심 기능")
    constraints: list[str] = Field(
        default_factory=list,
        description="비즈니스 규칙 및 기능적 제약조건"
    )
    technical_constraints: list[str] = Field(
        default_factory=list,
        description="사용자가 명시적으로 요구한 기술 또는 구현 제약조건"
    )
    data_requirements: list[DataRequirement] = Field(
        default_factory=list,
        description="프로젝트에서 관리해야하는 주요 데이터"
    )
    interfaces: list[str] = Field(
        default_factory=list,
        description="REST API, CLI, Web UI 등 외부 인터페이스 유형"
    )
    external_services: list[str] = Field(
        default_factory=list,
        description="사용자가 요구했거나 기능 수행에 반드시 필요한 외부 서비스"
    )