from fastapi import FastAPI, Path
from typing import Annotated

app = FastAPI()

# Изначально заданный словарь пользователей
users = {'1': 'Имя: Example, возраст: 18'}

@app.get("/users")
async def get_users():
    return users

@app.post("/user/{username}/{age}")
async def create_user(
    username: Annotated[str, Path(min_length=5, max_length=20)],
    age: Annotated[int, Path(ge=18, le=120)],
):
    new_id = str(max(map(int, users.keys())) + 1)
    users[new_id] = f"Имя: {username}, возраст: {age}"
    return {"message": f"User {new_id} is registered"}

@app.put("/user/{user_id}/{username}/{age}")
async def update_user(
    user_id: Annotated[int, Path(ge=1, le=100)],
    username: Annotated[str, Path(min_length=5, max_length=20)],
    age: Annotated[int, Path(ge=18, le=120)],
):
    user_id_str = str(user_id)
    if user_id_str not in users:
        return {"error": "Пользователь не найден"}

    users[user_id_str] = f"Имя: {username}, возраст: {age}"
    return {"message": f"The user {user_id} has been updated"}

@app.delete("/user/{user_id}")
async def delete_user(
    user_id: Annotated[int, Path(ge=1, le=100)]
):
    user_id_str = str(user_id)
    if user_id_str not in users:
        return {"error": "Пользователь не найден"}

    del users[user_id_str]
    return {"message": f"User {user_id} has been deleted"}

# Демонстрационные вызовы для проверки реализации
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
