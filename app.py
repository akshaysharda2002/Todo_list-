from fastapi import FastAPI, HTTPException,Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import sqlite3
from typing import List
from pydantic import BaseModel
from passlib.context import CryptContext

class Task(BaseModel):
    id: int = None
    title: str
    description: str = None
    done: bool = False

class User(BaseModel):
    username:str
    password:str

app = FastAPI()




pwd_context=CryptContext(schemes=["bcrypt"], deprecated="auto")
def get_pass_hash(password):
    return pwd_context.hash(password)

@app.post("/sign_up")
def sign_up(new_user:User):
    return {"message": "user created","username":new_user.username,"passsword":get_pass_hash(new_user.password)}









db = sqlite3.connect('test.db',check_same_thread=False)
@app.put("/create")
def create():
    cur=db.cursor()
    cur.execute("""create table task(id int,title varchar(20),description varchar(20),done bool);""")
    db.commit()
    cur.close()
    return {"message": "table created"}

@app.get("/")
def greet():
    return {"message": "Hello World!"}

@app.post("/tasks")
def create_task(task: Task): 
    task_dict = task.dict()
    # task_dict.pop("id", None)
    cur=db.cursor()
    cur.execute(f'''INSERT INTO tasks (title, description, done) VALUES ('{task_dict["title"]}','{task_dict["description"]}','{task_dict["done"]}')''')
    # task.id = task_id
    db.commit()
    cur.close()
    return JSONResponse(content=jsonable_encoder(task), status_code=201)

@app.get("/tasks", response_model=List[Task])
def read_tasks():
    cur=db.cursor()
    cur.execute("SELECT id, title, description, done FROM tasks")
    tasks=cur.fetchall()
    return JSONResponse(content=jsonable_encoder(tasks), status_code=200)
    

@app.get("/tasks/{task_id}", response_model=Task)
def read_task(task_id: int):
    cur=db.cursor()
    cur.execute(f"SELECT id, title, description, done FROM tasks WHERE id={task_id}")
    task=cur.fetchall()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return JSONResponse(content=jsonable_encoder(task), status_code=200)

# @app.put("/tasks/{task_id}", response_model=Task)
# async def update_task(task_id: int, task: Task):
#     task_dict = task.dict()
#     task_dict.pop("id", None)
#     await mysql_manager.execute("UPDATE tasks SET title=%(title)s, description=%(description)s, done=%(done)s WHERE id=%(id)s", dict(task_dict, id=task_id))
#     task.id = task_id
#     return task

# @app.delete("/tasks/{task_id}")
# async def delete_task(task_id: int):
#     result = await mysql_manager.execute("DELETE FROM tasks WHERE id=%s", (task_id,))
#     if not result:
#         raise HTTPException(status_code=404, detail="Task not found")
#     return JSONResponse(content={"message": "Task deleted"}, status_code=200)

