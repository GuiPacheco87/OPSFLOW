from datetime import datetime
from typing import Any
from pydantic import BaseModel,ConfigDict,EmailStr,Field
from .models import Role,WorkflowStatus,ExecutionStatus,TaskStatus
class ORM(BaseModel): model_config=ConfigDict(from_attributes=True)
class Register(BaseModel): organization_name:str=Field(min_length=2); name:str=Field(min_length=2); email:EmailStr; password:str=Field(min_length=8)
class Login(BaseModel): email:EmailStr; password:str
class Token(BaseModel): access_token:str; token_type:str="bearer"
class UserOut(ORM): id:str; organization_id:str; name:str; email:EmailStr; role:Role; active:bool
class UserCreate(BaseModel): name:str; email:EmailStr; password:str=Field(min_length=8); role:Role=Role.member
class StepCreate(BaseModel): name:str; order:int=Field(ge=1); assigned_role:Role=Role.manager; action_type:str="approval"; required:bool=True; sla_hours:int=Field(default=24,ge=1)
class StepOut(ORM): id:str; name:str; order:int; assigned_role:Role; action_type:str; required:bool; sla_hours:int
class WorkflowCreate(BaseModel): name:str; description:str=""; status:WorkflowStatus=WorkflowStatus.draft
class WorkflowUpdate(BaseModel): name:str|None=None; description:str|None=None; status:WorkflowStatus|None=None
class WorkflowOut(ORM): id:str; name:str; description:str; status:WorkflowStatus; created_at:datetime; steps:list[StepOut]=[]
class ExecutionCreate(BaseModel): workflow_id:str; request_data:dict[str,Any]=Field(default_factory=dict)
class ExecutionOut(ORM): id:str; workflow_id:str; status:ExecutionStatus; request_data:dict; started_at:datetime; completed_at:datetime|None
class TaskOut(ORM): id:str; execution_id:str; workflow_step_id:str; assigned_to:str|None; assigned_role:Role; status:TaskStatus; due_at:datetime; completed_at:datetime|None
class Decision(BaseModel): comment:str=""
class AuditOut(ORM): id:str; user_id:str; action:str; entity:str; entity_id:str; details:dict; created_at:datetime

