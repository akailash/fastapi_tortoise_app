from fastapi import FastAPI, HTTPException, Query
from tortoise.contrib.fastapi import register_tortoise
from tortoise.contrib.pydantic import pydantic_model_creator
from typing import List, Optional
from fastapi_tortoise_app.models import Task

app = FastAPI()

# Pydantic models for request/response validation
Task_Pydantic = pydantic_model_creator(Task, name="Task")
TaskIn_Pydantic = pydantic_model_creator(Task, name="TaskIn", exclude_readonly=True)

@app.post("/tasks", response_model=Task_Pydantic)
async def create_task(task: TaskIn_Pydantic):
    task_obj = await Task.create(**task.dict())
    return await Task_Pydantic.from_tortoise_orm(task_obj)

@app.get("/tasks/{task_id}", response_model=Task_Pydantic)
async def read_task(task_id: int):
    task = await Task_Pydantic.from_queryset_single(Task.get(id=task_id))
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.get("/tasks", response_model=List[Task_Pydantic])
async def read_tasks(is_completed: Optional[bool] = Query(None)):
    if is_completed is not None:
        tasks = await Task_Pydantic.from_queryset(Task.filter(is_completed=is_completed))
    else:
        tasks = await Task_Pydantic.from_queryset(Task.all())
    return tasks

@app.put("/tasks/{task_id}", response_model=Task_Pydantic)
async def update_task(task_id: int, task: TaskIn_Pydantic):
    await Task.filter(id=task_id).update(**task.dict(exclude_unset=True))
    updated_task = await Task_Pydantic.from_queryset_single(Task.get(id=task_id))
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task

@app.delete("/tasks/{task_id}", response_model=dict)
async def delete_task(task_id: int):
    deleted_count = await Task.filter(id=task_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"deleted": deleted_count}

# Tortoise ORM configuration
register_tortoise(
    app,
    db_url="sqlite://:memory:",
    modules={"models": ["fastapi_tortoise_app.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
