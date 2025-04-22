from fastapi import APIRouter, HTTPException
from models import Todo
from database import db
from bson import ObjectId

router = APIRouter()

def todo_serializer(todo) -> dict:
    return {
        "id": str(todo["_id"]),
        "title": todo["title"],
        "description": todo.get("description", ""),
        "done": todo["done"]
    }

@router.get("/todos")
async def get_todos():
    todos = await db.tasks.find().to_list(100)
    return [todo_serializer(todo) for todo in todos]

@router.post("/todos")
async def create_todo(todo: Todo):
    todo_dict = todo.dict()
    result = await db.tasks.insert_one(todo_dict)
    created_todo = await db.tasks.find_one({"_id": result.inserted_id})
    return todo_serializer(created_todo)

@router.put("/todos/{todo_id}")
async def update_todo(todo_id: str, todo: Todo):
    updated_todo = await db.tasks.find_one_and_update(
        {"_id": ObjectId(todo_id)},
        {"$set": todo.dict()},
        return_document=True
    )
    if updated_todo:
        return todo_serializer(updated_todo)
    raise HTTPException(status_code=404, detail="Todo not found")

@router.delete("/todos/{todo_id}")
async def delete_todo(todo_id: str):
    deleted_todo = await db.tasks.find_one_and_delete({"_id": ObjectId(todo_id)})
    if deleted_todo:
        return todo_serializer(deleted_todo)
    raise HTTPException(status_code=404, detail="Todo not found")
