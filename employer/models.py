from pydantic import BaseModel


class Job(BaseModel):
    Name: str
    Description: str
    Salary: str
    Location: str
    Category: str
    Experience: str
    Education: str
    Skills: str
    JobType: str
    JobFunction: str
    Industry: str
    Role: str
    EmploymentType: str
    CompanyName: str
    CompanySize: str
    CompanyType: str

    def __str__(self):
        return self.Name


class JobSearch(BaseModel):
    Name: str
    Location: str
    Category: str
    Experience: str
    Education: str
    Skills: str
    JobType: str
    JobFunction: str
    Industry: str
    Role: str
    EmploymentType: str
    CompanyName: str
    CompanySize: str
    CompanyType: str


from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table

from database import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, unique=True, index=True)
    Name = Column(String(500), index=False)
    Description = Column(String(1000), index=False)


class Employer(Base):
    __tablename__ = "employers"

    id = Column(Integer, primary_key=True, unique=True, index=True)
    Name = Column(String(500), index=False)
    # Description = Column(String, index=False)
    # Salary = Column(String, index=False)
    # Location = Column(String, index=False)
    # Category = Column(String, index=False)
    # Experience = Column(String, index=False)
    # Education = Column(String, index=False)
    # Skills = Column(String, index=False)
    # JobType = Column(String, index=False)
    # JobFunction = Column(String(length=100), index=False)
    # Industry = Column(String, index=False)
    # Role = Column(String, index=False)
    # EmploymentType = Column(String, index=False)
    # CompanyName = Column(String, index=False)
    # CompanySize = Column(String, index=False)
    # CompanyType = Column(String, index=False)
