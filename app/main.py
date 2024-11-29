from fastapi import FastAPI, APIRouter, Request
from app.routers import users, auth, friends, expenses, transaction, dashboard
import time
from datetime import datetime

app = FastAPI()


@app.middleware("http")
async def add_process_time(request: Request, call_next):

    d = {
        "intiationtime": datetime.now(),
        "method": request.method,
        "url": request.url,
        "client_detail": request.client,
    }

    response = await call_next(request)
    print(response)
    d["status_code"] = response.status_code
    d["responce_timestamp"] = datetime.now()
    d["duration"] = d["responce_timestamp"] - d["intiationtime"]

    print(d)

    return response


app.include_router(users.router)
app.include_router(auth.router)
app.include_router(friends.router)
app.include_router(expenses.router)
app.include_router(transaction.router)
app.include_router(dashboard.router)

# @app.get("/")
# async def root():
#     return {"message": "Hello World"}
