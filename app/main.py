from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette import status

from app.models import Base
from app.database import engine
from app.router import auth, todos, admin, user
from fastapi.staticfiles import StaticFiles

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="./static"), name="static")

@app.get("/", response_class=HTMLResponse)
def test(request: Request):
    return RedirectResponse(url="/todos/todo-page", status_code=status.HTTP_302_FOUND)
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/healthy")
def health_check():
    return {"status": "Healthy"}

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(user.router)

