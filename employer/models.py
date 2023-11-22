from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    Float,
    Date,
)
from sqlalchemy_utils import EmailType, PasswordType
from database import Base

from sqlalchemy.orm import relationship


class JobApplicant(Base):
    __tablename__ = "job_jobseeker"
    Job_id = Column(Integer, ForeignKey("jobs.id"), primary_key=True, index=True)
    Applicant_id = Column(
        Integer, ForeignKey("job_seeker.id"), primary_key=True, index=True
    )
    Status = Column(String(500), index=False)
    Rejected = Column(Boolean, default=False, index=False)
    In_considiration = Column(Boolean, default=False, index=False)


class JobSeeker(Base):
    __tablename__ = "job_seeker"
    id = Column(Integer, primary_key=True, unique=True, index=True)
    name = Column(String(500), index=False)
    email = Column(EmailType, index=False)
    age = Column(Integer, index=False)
    education = relationship("Education", backref="job_seeker", lazy="dynamic")
    field = Column(String(500), index=False)
    career_experience = relationship(
        "CareerExperience", backref="job_seeker", lazy="dynamic"
    )
    interests = Column(String)
    skills = Column(String)
    languages = Column(String)
    certifications = Column(String)
    hobbies = Column(String)
    Photos = relationship("Photos", backref="job_seeker", lazy="dynamic")
    jobs_applied = Column(String)
    Expected_salary = Column(Float, index=False)


class Photos(Base):
    __tablename__ = "photos"
    id = Column(Integer, primary_key=True, unique=True, index=True)
    url = Column(String(500), index=False)
    job_seeker_id = Column(
        Integer, ForeignKey("job_seeker.id"), index=False, unique=False
    )
    uploaded_at = Column(Date, index=False)
    name = Column(String(500), index=False)


class Education(Base):
    __tablename__ = "education"
    id = Column(Integer, primary_key=True, unique=True, index=True)
    institution_name = Column(String(500), index=False)
    degree = Column(String(500), index=False)
    field_of_study = Column(String(500), index=False)
    grade = Column(Float, index=False)
    education_start_date = Column(Date, index=False)
    education_end_date = Column(Date, index=False)
    description = Column(String(2000), index=False)
    skills_gained = Column(String(2000), index=False)
    job_seeker_id = Column(Integer, ForeignKey("job_seeker.id"), index=False)


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, unique=True, index=True)
    name = Column(String(500), index=False)
    description = Column(String(1000), index=False)
    experience_required = Column(Integer, default=0, index=False)
    qualification_required = Column(String(500), index=False)
    salary = Column(Float, index=False)
    is_open = Column(Boolean, default=True, index=False)
    company = Column(ForeignKey("companies.id"), index=False)
    employer = Column(ForeignKey("employers.id"), index=False)

    def can_employer_access(self, employer_id):
        return self.employer != employer_id


class Company(Base):
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True, unique=True, index=True)
    company_name = Column(String(500), index=False)
    number_of_employee = Column(Integer, index=False)
    industry = Column(String(500), index=False)
    type = Column(String(500), index=False)
    telephone = Column(Integer, index=False)
    website = Column(String(500), index=False)
    established = Column(Date, index=False)
    country = Column(String(500), index=False)
    address = Column(String(500), index=False)
    email = Column(EmailType, index=False)


class Employer(Base):
    __tablename__ = "employers"

    id = Column(Integer, primary_key=True, unique=True, index=True)
    name = Column(String(500), index=False)
    company = Column(ForeignKey("companies.id"), index=False)
    email = Column(EmailType, index=False)
    additional_info = Column(String, index=False)
    password = Column(
        PasswordType(schemes=["pbkdf2_sha512", "md5_crypt"], deprecated=["md5_crypt"]),
        index=False,
    )


class CareerExperience(Base):
    __tablename__ = "career_experience"
    id = Column(Integer, primary_key=True, unique=True, index=True)
    company_name = Column(String(500), index=False)
    job_title = Column(String(500), index=False)
    period = Column(String(500), index=False)
    skilled_gained = Column(String)
    contributions = Column(String, index=False)
    achievements = Column(String, index=False)
    salary = Column(Float, index=False)
    job_seeker_id = Column(Integer, ForeignKey("job_seeker.id"), index=False)
