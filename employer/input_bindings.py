from pydantic import BaseModel
from datetime import date


class Job(BaseModel):
    name: str = ""
    description: str = ""
    salary: float = 0.0
    experience_required: int = 0
    qualification_required: str = ""

    # Education: str = ""
    # Skills: str = ""
    # JobType: str = ""
    # JobFunction: str = ""
    # Industry: str = ""


from time import time


class MessageBody(BaseModel):
    message: str = ""


class Company(BaseModel):
    company_name: str
    number_of_employee: int
    industry: str
    type: str
    telephone: int
    website: str = ""
    established: date
    country: str
    address: str
    email: str
