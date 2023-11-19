from typing import Union, Annotated
from pydantic import BaseModel
from fastapi import FastAPI, Cookie, Request, Depends, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, ORJSONResponse
import time

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
    if request.cookies.get("Auth"):
        if valid_auth_token():
            response = await call_next(request)
            return response
    return Response(status_code=401, content="Not Authorized")


def valid_auth_token():
    return True


templates = Jinja2Templates(directory="./templates/")


@app.post("/job", response_class=HTMLResponse, dependencies=[Depends(Auth_Middleware)])
async def create_job(request: Request, job: input_bindings.Job):
    job = models.Job(**job.model_dump())
    db.add(job)
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
