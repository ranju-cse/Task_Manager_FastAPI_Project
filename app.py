from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field
from typing import Annotated,Literal
import json
#creating an app instance
app=FastAPI()

class Task(BaseModel):
    id:Annotated[str,Field(...,description="Enter Task Id")]
    title:Annotated[str,Field(...,description="Title of the Task")]
    description:Annotated[str,Field(...,description="Task description")]
    status:Annotated[Literal['Complete','Pending','In Progress'],Field(...,description="Status of Task")]
    


def load_data():
    with open('Task.json','r') as f:
     return json.load(f) 
 
def save_data(data):
     with open('Task.json','w') as f:
         json.dump(data,f)
           
@app.post('/create')
def create_task(task:Task):
    data=load_data()
    print(data)
#check if patient already exist
    if task.id in data:
        raise HTTPException(status_code=400,detail='Task exist already')
    
    #If not exist add to the Db
    data[task.id]=task.model_dump(exclude=['id'])
     # Save updated data
    save_data(data)

    return JSONResponse(content={
        "message": "Task created successfully",
        "task_id": task.id
    })
    


