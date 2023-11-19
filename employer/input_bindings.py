from pydantic import BaseModel


class Job(BaseModel):
    Name: str = ""
    Description: str = ""
    Salary: float = 0.0
    Experience_required: int = 0
    Qualification_required: str = ""

    # Education: str = ""
    # Skills: str = ""
    # JobType: str = ""
    # JobFunction: str = ""
    # Industry: str = ""
