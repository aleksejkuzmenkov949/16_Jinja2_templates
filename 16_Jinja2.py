from fastapi import FastAPI, Path, HTTPException, Request
from pydantic import BaseModel, Field
from typing import List, Annotated
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import uvicorn

# Создаем объект Jinja2Templates
templates = Jinja2Templates(directory="templates")
app = FastAPI()

# Пустой список пользователей
users = []

class User(BaseModel):
    id: int
    username: str = Field(..., min_length=5, max_length=20)
    age: int = Field(..., ge=18, le=120)

@app.get("/", response_class=HTMLResponse)
async def read_users(request: Request):
    return templates.TemplateResponse("users.html", {"request": request, "users": users})

@app.get("/users/{user_id}", response_class=HTMLResponse)
async def get_user(request: Request, user_id: Annotated[int, Path(ge=1, le=100)]):
    user = next((user for user in users if user.id == user_id), None)
    if user is None:
        raise HTTPException(status_code=404, detail="User was not found")
    return templates.TemplateResponse("users.html", {"request": request, "user": user})

@app.post("/user/{username}/{age}", response_model=User)
async def create_user(username: Annotated[str, Path(min_length=5, max_length=20)], age: Annotated[int, Path(ge=18, le=120)]):
    new_id = users[-1].id + 1 if users else 1
    new_user = User(id=new_id, username=username, age=age)
    users.append(new_user)
    return new_user

@app.put("/user/{user_id}/{username}/{age}", response_model=User)
async def update_user(user_id: Annotated[int, Path(ge=1, le=100)], username: Annotated[str, Path(min_length=5, max_length=20)], age: Annotated[int, Path(ge=18, le=120)]):
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user
    raise HTTPException(status_code=404, detail="User was not found")

@app.delete("/user/{user_id}", response_model=User)
async def delete_user(user_id: Annotated[int, Path(ge=1, le=100)]):
    for user in users:
        if user.id == user_id:
            users.remove(user)
            return user
    raise HTTPException(status_code=404, detail="User was not found")

# Создаем пользователей
@app.on_event("startup")
async def startup_event():
    users.append(User(id=1, username="UrbanUser", age=24))
    users.append(User(id=2, username="UrbanTest", age=22))
    users.append(User(id=3, username="Capybara", age=60))

# Демонстрационные вызовы для проверки реализации
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
