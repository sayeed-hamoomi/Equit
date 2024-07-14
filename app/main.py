from fastapi import FastAPI,APIRouter
from app.routers import users,auth,friends,expenses


app=FastAPI()

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(friends.router)
app.include_router(expenses.router)

# @app.get("/")
# async def root():
#     return {"message": "Hello World"}