from fastapi import FastAPI, HTTPException
from models import Todo, Todo_Pydantic, TodoIn_Pydantic
from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise
from pydantic import BaseModel

class Message(BaseModel):
    message: str

app = FastAPI()

@app.get("/")
async def hello():
    return {"hello": "world"}


@app.post("/todo", response_model=Todo_Pydantic)
async def create(todo: TodoIn_Pydantic):  # type: ignore
    try:
        obj = await Todo.create(**todo.model_dump(exclude_unset=True))
        return await Todo_Pydantic.from_tortoise_orm(obj)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/todo/{id}", response_model=TodoIn_Pydantic, responses={404: {"model": HTTPNotFoundError}})
async def get_one(id: int):
    return await TodoIn_Pydantic.from_queryset_single(Todo.get(id= id))


@app.put("/todo/{id}", response_model=Todo_Pydantic, responses={404: {"model": HTTPNotFoundError}})
async def update_one(id: int, todo: TodoIn_Pydantic): # type: ignore
    await Todo.filter(id = id).update(**todo.model_dump(exclude_unset=True))
    return await Todo_Pydantic.from_queryset_single(Todo.get(id=id))


@app.delete("/todo/{id}", response_model=Message, responses={404: {"model": HTTPNotFoundError}})
async def delete_one(id: int): # type: ignore
    delete_obj = await Todo.filter(id = id).delete()
    if not delete_obj:
        raise HTTPException(status_code=404, detail="Todo not found")
    return Message(message="Successfully deleted")
    


register_tortoise(
    app,
    db_url = "postgres://postgres:Adrien.ldg02@localhost:5432/full_stack_db",
    modules={"models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True
)