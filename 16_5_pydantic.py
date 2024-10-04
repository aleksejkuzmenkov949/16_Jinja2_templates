from fastapi import FastAPI, Path, HTTPException
from pydantic import BaseModel, Field
from typing import List, Annotated

app = FastAPI()

# Пустой список пользователей
users = []

class User(BaseModel):
    id: int
    username: str = Field(..., min_length=5, max_length=20)
    age: int = Field(..., ge=18, le=120)

@app.get("/users", response_model=List[User])
async def get_users():
    return users

@app.post("/user/{username}/{age}", response_model=User)
async def create_user(
    username: Annotated[str, Path(min_length=5, max_length=20)],
    age: Annotated[int, Path(ge=18, le=120)],
):
    new_id = users[-1].id + 1 if users else 1
    new_user = User(id=new_id, username=username, age=age)
    users.append(new_user)
    return new_user

@app.put("/user/{user_id}/{username}/{age}", response_model=User)
async def update_user(
    user_id: Annotated[int, Path(ge=1, le=100)],
    username: Annotated[str, Path(min_length=5, max_length=20)],
    age: Annotated[int, Path(ge=18, le=120)],
):
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user
    raise HTTPException(status_code=404, detail="User was not found")

@app.delete("/user/{user_id}", response_model=User)
async def delete_user(
    user_id: Annotated[int, Path(ge=1, le=100)]
):
    for user in users:
        if user.id == user_id:
            users.remove(user)
            return user
    raise HTTPException(status_code=404, detail="User was not found")

# Демонстрационные вызовы для проверки реализации
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)