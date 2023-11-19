from typing import Union, Annotated
from pydantic import BaseModel
from fastapi import FastAPI, Cookie, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from database import Base, engine, get_db
from sqlalchemy.orm import Session
import input_bindings
import models

# import render_template


models.Base.metadata.create_all(bind=engine)
db = get_db()
app = FastAPI()


async def Auth_Middleware(request):
    print(request.headers)
    if "auth" in request.headers:
        if valid_auth_token():
            print("In Auth middleware")
            return request
    raise {"error": "not authorized"}


def valid_auth_token():
    return True


templates = Jinja2Templates(directory="./templates/")


@app.post("/job", response_class=HTMLResponse, dependencies=[Depends(Auth_Middleware)])
async def create_job(request: Request, job: input_bindings.Job):
    job = models.Job(**job.model_dump())
    db.add(job)
    print(job.__dict__)
    db.commit()
    return templates.TemplateResponse("test.html", {"request": request})


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
