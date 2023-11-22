from typing import Union, Annotated
from pydantic import BaseModel
from fastapi import FastAPI, Cookie, Request, Depends, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, ORJSONResponse
import time
from auth import get_info_from_token

# impoer httpresponse

from database import Base, engine, get_db
from sqlalchemy.orm import Session
import input_bindings
import models

# import render_template


models.Base.metadata.create_all(bind=engine)
db = get_db()
app = FastAPI()


@app.middleware("http")
async def TimeTakenMiddleware(request: Request, call_next: callable):
    """
    response
    """

    start_time = time.time()
    response = await call_next(request)

    # add json to response for time taken
    response.headers["Content-Type"] = "application/json"
    # write data response
    response.headers["X-Time-Taken"] = str(time.time() - start_time)
    return response


@app.middleware("http")
async def Auth_Middleware(request: Request, call_next):
    print("In Auth MIddleware")
    if request.cookies.get("auth"):
        token_decoded = get_info_from_token(request.cookies.get("auth"))

        if token_decoded != False and token_decoded["role"] == "employer":
            response = await call_next(request)
            path = request.url.path
            if path == "/docs" or path == "/redoc":
                response.headers["Content-Type"] = "text/html"
                return response
            if response.headers.get("Content-Type") != "text/html":
                response.headers["Content-Type"] = "application/json"
            return response
    return Response(status_code=401, content="Not Authorized")


def valid_auth_token():
    return True


templates = Jinja2Templates(directory="./templates/")


@app.post("/create_test_employer", response_class=HTMLResponse)
async def create_test_employer(request: Request):
    employer = models.Employer()
    employer.name = "test"
    employer.email = "hamidovaslon1@gmail.com"
    employer.password = "test"
    employer.additional_info = "test"
    employer.company = 1
    db.add(employer)
    db.commit()


# CRUD for company
@app.post("/company")
async def create_company(request: Request, company: input_bindings.Company):
    company = models.Company(**company.model_dump())
    db.add(company)
    db.commit()
    return company.__dict__


@app.get("/company/{company_id}")
async def get_company(request: Request, company_id: int):
    company = db.query(models.Company).filter_by(id=company_id).first()
    if company == None:
        return Response(
            status_code=404, content="{'error': 'The company with this id not found'}"
        )
    return company.__dict__


@app.put("/company/{company_id}")
async def edit_company(
    request: Request, company_input: input_bindings.Company, company_id: int
):
    company = db.query(models.Company).filter_by(id=company_id).first()
    if company == None:
        return Response(
            status_code=404, content="{'error': 'The company with this id not found'}"
        )
    company_info = company_input.model_dump()
    for key in company_info:
        setattr(company, key, company_info[key])

    db.commit()
    return company.__dict__


@app.delete("/company/{company_id}")
async def delete_company(request: Request, company_id: int):
    return Response(status_code=501, content="Not Implemented")


@app.post("/job", response_class=HTMLResponse)
async def create_job(request: Request, job: input_bindings.Job):
    job = models.Job(**job.model_dump())
    token_info = get_info_from_token(request.cookies.get("auth"))
    job.employer = token_info["id"]
    employer = db.query(models.Employer).filter_by(id=token_info["id"]).first()
    job.company = employer.company
    db.add(job)
    db.commit()
    return HTMLResponse(content="Job Created with id " + str(job.id))


# to edit the job details
@app.put("/job/{job_id}")
async def edit_job(request: Request, job_input: input_bindings.Job, job_id: int):
    token_info = get_info_from_token(request.cookies.get("auth"))
    job = db.query(models.Job).filter_by(id=job_id).first()
    if job == None:
        return Response(
            status_code=404, content="{'error': 'The job with this id not found'}"
        )
    if not job.can_employer_access(token_info["id"]):
        return Response(
            status_code=401,
            content="Not Authorized!!!! You are not the owner of this job",
        )

    # update the job
    job.name = job_input.name
    job.description = job_input.description
    job.salary = job_input.salary
    job.qualification_required = job_input.qualification_required
    job.experience_required = job_input.experience_required
    # update the job
    db.commit()
    return job.__dict__


@app.delete("/job/{job_id}")
async def delete_job(request: Request, job_id: int):
    token_info = get_info_from_token(request.cookies.get("auth"))
    job = db.query(models.Job).filter_by(id=job_id).first()
    if job == None:
        return Response(
            status_code=404, content="{'error': 'The job with this id not found'}"
        )
    if job.Employer != int(token_info["id"]):
        return Response(
            status_code=401,
            content="Not Authorized!!!! You are not the owner of this job",
        )
    try:
        db.delete(job)
    except:
        return Response(
            status_code=500, content="Internal Server Error while deleting the job"
        )
    db.commit()
    return job.__dict__


@app.get("job/my")
async def query_my_jobs(request: Request):
    response = {}
    token_info = get_info_from_token(request.cookies.get("auth"))
    jobs = db.query(models.Job).filter_by(employer=token_info["id"]).all()
    response["jobs"] = jobs
    return response


@app.get("/job/all")
async def query_jobs(request: Request):
    response = {}
    jobs = db.query(models.Job).filter(models.Job.is_open == True).all()
    response["jobs"] = jobs
    print(response)
    return response


@app.put("/job/{job_id}/close")
async def close_job(request: Request, job_id: int):
    token_info = get_info_from_token(request.cookies.get("auth"))
    job = db.query(models.Job).filter_by(id=job_id).first()
    if job == None:
        return Response(
            status_code=404, content="{'error': 'The job with this id not found'}"
        )
    if not job.can_employer_access(token_info["id"]):
        return Response(
            status_code=401,
            content="Not Authorized!!!! You are not the owner of this job",
        )
    if job.is_open:
        job.is_open = False
    else:
        return {
            "error": "The job is already closed",
        }
    db.commit()
    return job
