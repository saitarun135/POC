from fastapi import FastAPI
from user import user_router
from todo import todo_router
import events.todo_event

app = FastAPI()

app.include_router(user_router,tags=['user'])
app.include_router(todo_router,prefix='/todo', tags=['todos'])