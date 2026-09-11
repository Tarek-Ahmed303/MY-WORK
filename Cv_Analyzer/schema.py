from typing import Optional
from pydantic import BaseModel, Field


class Candidate(BaseModel):

    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    portfolio: Optional[str] = None


class Education(BaseModel):

    degree: Optional[str] = None
    institution: Optional[str] = None
    field: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    gpa: Optional[str] = None


class Experience(BaseModel):

    job_title: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    description: Optional[str] = None

    technologies: list[str] = Field(
        default_factory=list
    )


class Skills(BaseModel):

    technical: list[str] = Field(
        default_factory=list
    )

    soft: list[str] = Field(
        default_factory=list
    )


class Project(BaseModel):

    name: Optional[str] = None
    description: Optional[str] = None

    technologies: list[str] = Field(
        default_factory=list
    )

    url: Optional[str] = None


class Certification(BaseModel):

    name: Optional[str] = None
    issuer: Optional[str] = None
    date: Optional[str] = None


class Language(BaseModel):

    language: Optional[str] = None
    proficiency: Optional[str] = None


class Career(BaseModel):

    job_titles: list[str] = Field(
        default_factory=list
    )

    years_of_experience: float = 0


class Quality(BaseModel):

    completeness: int = 0
    readability: int = 0
    structure: int = 0

    formatting_issues: list[str] = Field(
        default_factory=list
    )


class InterviewContext(BaseModel):

    projects: list[str] = Field(
        default_factory=list
    )

    technologies: list[str] = Field(
        default_factory=list
    )

    experience_topics: list[str] = Field(
        default_factory=list
    )

    claims_to_verify: list[str] = Field(
        default_factory=list
    )


class Resume(BaseModel):

    resume_id: str

    candidate: Candidate

    summary: Optional[str] = None

    education: list[Education] = Field(
        default_factory=list
    )

    experience: list[Experience] = Field(
        default_factory=list
    )

    skills: Skills

    projects: list[Project] = Field(
        default_factory=list
    )

    certifications: list[Certification] = Field(
        default_factory=list
    )

    languages: list[Language] = Field(
        default_factory=list
    )

    career: Career

    quality: Quality

    interview_context: InterviewContext