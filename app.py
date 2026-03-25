from fastapi import FastAPI, HTTPException,Path
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field
from typing import Annotated,Literal,Optional
import json
#creating an app instance
app=FastAPI()

class Task(BaseModel):
    Task_id:Annotated[str,Field(...,description="Enter Task Id")]
    title:Annotated[str,Field(...,description="Title of the Task")]
    description:Annotated[str,Field(...,description="Task description")]
    status:Annotated[Literal['Complete','Pending','In Progress'],Field(...,description="Status of Task")]
    

#Creating a pydantic class to update task records
class TaskUpdate(BaseModel):
    title:Annotated[Optional[str],Field(default=None)]
    description:Annotated[Optional[str],Field(default=None)]
    status:Annotated[Optional[Literal['Complete','Pending','In Progress']],Field(default=None)]
    

def load_data():
    with open('Task.json','r') as f:
        return json.load(f) 
 
def save_data(data):
    with open('Task.json','w') as f:
        json.dump(data,f)
         
#Create  a new Task -(POST Method)         
@app.post('/create')
def create_task(task:Task):
    data=load_data()
    print(data)
#check if Task already exist
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
 
 
 
#Update existing task details by using their id (put Method)  
@app.put('/Edit/{Task_id}')
def view_task(Task_id:str=Path(...), task_update:TaskUpdate=None):
    data=load_data()

    if Task_id not in data:
        raise HTTPException(status_code=404,detail="Task id not found")

    #get current task
    existing_task=data[Task_id]
    updated_task=task_update.model_dump(exclude_unset=True)#exclude_unset=True → only includes fields user actually sent
    
    for key,value in updated_task.items():
        existing_task[key]=value
    
    #save data
    save_data(data)
    return JSONResponse(status_code=200,content={'message':'patient updated'})

    
#Retrieve Tasks by id
@app.get('/View_tasks/{task_id}')
def get_task(task_id:str=Path(...,description='ID of the task in DB',example='T001')):
    data=load_data()
    
    if task_id not in data:
        raise HTTPException(status_code=404,detail="Task id not found")
    return data[task_id]


    
#Delete task
@app.delete('/delete/{task_id}')
def delete_data(task_id:str):
    data=load_data()
    
    if task_id not in data:
        raise HTTPException(status_code=404,detail='Task not found')
    
    if "id" in data[task_id]:
        del data[task_id]['id']
        save_data(data)
        
    del data[task_id]
    save_data(data)
    
    return{
        'message':'Task deleted Successfully',
        'deleted_task':delete_data
    }

