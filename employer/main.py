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


@app.post("/job", response_class=HTMLResponse)
async def create_job(request: Request, job: input_bindings.Job):
    job = models.Job(**job.model_dump())
    token_info = get_info_from_token(request.cookies.get("auth"))
    job.Employer = token_info["id"]
    employer = db.query(models.Employer).filter_by(id=token_info["id"]).first()
    job.Company = 1
    db.add(job)
    db.commit()
    return HTMLResponse(content="Job Created with id " + str(job.id))


@app.put("/job/{job_id}")
async def edit_job(request: Request, job_input: input_bindings.Job, job_id: int):
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

    # update the job
    job.Name = job_input.Name
    job.Description = job_input.Description
    job.Salary = job_input.Salary
    job.Qualification_required = job_input.Qualification_required
    job.Experience_required = job_input.Experience_required
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


@app.get("/job")
async def query_jobs(request: Request):
    response = {}
    jobs = db.query(models.Job).all()
    response["jobs"] = jobs
    print(response)
    return response


async def create_job(request: Request):
    # render the html page
    # return the html page
    print(request.headers)
    return templates.TemplateResponse("test.html", {"request": request})
