from pydantic import BaseModel


class Job(BaseModel):
    Name: str = ""
    Description: str = ""
    # Salary: str = ""
    # Location: str = ""
    # Category: str = ""
    # Experience: str = ""

    # Education: str = ""
    # Skills: str = ""
    # JobType: str = ""
    # JobFunction: str = ""
    # Industry: str = ""
