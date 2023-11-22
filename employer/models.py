from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    Float,
    Date,
)
from sqlalchemy_utils import EmailType, PasswordType, ChoiceType, Choice
from database import Base

from sqlalchemy.orm import relationship


class JobApplicant(Base):
    __tablename__ = "job_jobseeker"
    job_id = Column(Integer, ForeignKey("jobs.id"), primary_key=True, index=True)
    applicant_id = Column(
        Integer, ForeignKey("job_seeker.id"), primary_key=True, index=True
    )
    STATUS_TYPES = [
        ("pending", "pending"),
        ("accepted", "accepted"),
        ("rejected", "rejected"),
    ]
    status = Column(ChoiceType(choices=STATUS_TYPES), index=False)

    applicant_cover_letter = Column(String, index=False)


from datetime import datetime


class ChatJobSeekerEmployer(Base):
    __tablename__ = "chats_jobseeker_employer"
    id = Column(Integer, primary_key=True, unique=True, index=True)
    job_seeker_id = Column(Integer, ForeignKey("job_seeker.id"), index=False)
    employer_id = Column(Integer, ForeignKey("employers.id"), index=False)

    def open_chat(self, job_seeker_id, employer_id):
        chat = ChatJobSeekerEmployer(
            job_seeker_id=job_seeker_id, employer_id=employer_id
        )
        return chat

    def write_message_employer(self, message_body):
        return Message(
            sender=self.employer_id,
            sender_type="employer",
            message_body=message_body,
            sent_at=datetime.now(),
            reciever=self.job_seeker_id,
            reciever_type="job_seeker",
            read=False,
            chat_id=self.id,
        )

    def write_message_job_seeker(self, message_body):
        return Message(
            chat_id=self.id,
            sender=self.job_seeker_id,
            sender_type="job_seeker",
            message_body=message_body,
            sent_at=datetime.now(),
            reciever=self.employer_id,
            reciever_type="employer",
            read=False,
        )


class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, unique=True, index=True)
    chat_id = Column(Integer, ForeignKey("chats_jobseeker_employer.id"), index=False)
    TYPES = [
        ("job_seeker", "job_seeker"),
        ("employer", "employer"),
        ("admin", "admin"),
    ]
    sender = Column(Integer, index=False)
    sender_type = Column(ChoiceType(TYPES), index=False)
    message_body = Column(String, index=False)
    sent_at = Column(Date, index=False)
    reciever = Column(Integer, index=False)
    reciever_type = Column(ChoiceType(TYPES), index=False)
    read = Column(Boolean, default=False, index=False)


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
