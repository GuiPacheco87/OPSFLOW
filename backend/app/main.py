from fastapi import Depends,FastAPI,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func,select
from sqlalchemy.orm import Session
from .config import settings
from .database import get_db
from .dependencies import current_user,require
from . import models as m,schemas as s,services
from .security import create_token,hash_password
app=FastAPI(title="OpsFlow API",version="0.1.0")
app.add_middleware(CORSMiddleware,allow_origins=settings.cors_origins.split(","),allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
A="/api/v1"
@app.get("/health")
def health(): return {"status":"ok"}
@app.post(A+"/auth/register",response_model=s.Token,status_code=201)
def register(data:s.Register,db:Session=Depends(get_db)):
    u=services.register(db,data); return {"access_token":create_token(u.id,u.organization_id)}
@app.post(A+"/auth/login",response_model=s.Token)
def login(data:s.Login,db:Session=Depends(get_db)):
    u=services.authenticate(db,data.email,data.password); return {"access_token":create_token(u.id,u.organization_id)}
@app.get(A+"/me",response_model=s.UserOut)
def me(user:m.User=Depends(current_user)): return user
@app.get(A+"/users",response_model=list[s.UserOut])
def users(user:m.User=Depends(require(m.Role.admin,m.Role.manager)),db:Session=Depends(get_db)): return db.scalars(select(m.User).where(m.User.organization_id==user.organization_id)).all()
@app.post(A+"/users",response_model=s.UserOut,status_code=201)
def create_user(data:s.UserCreate,user:m.User=Depends(require(m.Role.admin)),db:Session=Depends(get_db)):
    if db.scalar(select(m.User).where(m.User.organization_id==user.organization_id,func.lower(m.User.email)==data.email.lower())): raise HTTPException(409,"E-mail já existe")
    obj=m.User(organization_id=user.organization_id,name=data.name,email=data.email.lower(),password_hash=hash_password(data.password),role=data.role); db.add(obj); db.flush(); services.audit(db,user,"created","user",obj.id); db.commit(); return obj
@app.get(A+"/workflows",response_model=list[s.WorkflowOut])
def workflows(user:m.User=Depends(current_user),db:Session=Depends(get_db)): return db.scalars(select(m.Workflow).where(m.Workflow.organization_id==user.organization_id).order_by(m.Workflow.created_at.desc())).unique().all()
@app.post(A+"/workflows",response_model=s.WorkflowOut,status_code=201)
def create_workflow(data:s.WorkflowCreate,user:m.User=Depends(require(m.Role.admin,m.Role.manager)),db:Session=Depends(get_db)):
    obj=m.Workflow(organization_id=user.organization_id,created_by=user.id,**data.model_dump()); db.add(obj); db.flush(); services.audit(db,user,"created","workflow",obj.id); db.commit(); return obj
@app.get(A+"/workflows/{workflow_id}",response_model=s.WorkflowOut)
def workflow(workflow_id:str,user:m.User=Depends(current_user),db:Session=Depends(get_db)): return services.tenant(db,m.Workflow,user,workflow_id)
@app.put(A+"/workflows/{workflow_id}",response_model=s.WorkflowOut)
def update_workflow(workflow_id:str,data:s.WorkflowUpdate,user:m.User=Depends(require(m.Role.admin,m.Role.manager)),db:Session=Depends(get_db)):
    obj=services.tenant(db,m.Workflow,user,workflow_id)
    for key,value in data.model_dump(exclude_none=True).items(): setattr(obj,key,value)
    services.audit(db,user,"updated","workflow",obj.id); db.commit(); return obj
@app.post(A+"/workflows/{workflow_id}/steps",response_model=s.StepOut,status_code=201)
def add_step(workflow_id:str,data:s.StepCreate,user:m.User=Depends(require(m.Role.admin,m.Role.manager)),db:Session=Depends(get_db)):
    w=services.tenant(db,m.Workflow,user,workflow_id); step=m.WorkflowStep(workflow_id=w.id,**data.model_dump()); db.add(step); db.flush(); services.audit(db,user,"created","workflow_step",step.id); db.commit(); return step
@app.post(A+"/executions",response_model=s.ExecutionOut,status_code=201)
def start(data:s.ExecutionCreate,user:m.User=Depends(current_user),db:Session=Depends(get_db)): return services.start_execution(db,user,data)
@app.get(A+"/executions",response_model=list[s.ExecutionOut])
def executions(user:m.User=Depends(current_user),db:Session=Depends(get_db)): return db.scalars(select(m.WorkflowExecution).where(m.WorkflowExecution.organization_id==user.organization_id).order_by(m.WorkflowExecution.started_at.desc())).all()
@app.get(A+"/tasks",response_model=list[s.TaskOut])
def tasks(user:m.User=Depends(current_user),db:Session=Depends(get_db)):
    services.mark_overdue(db,user.organization_id)
    q=select(m.Task).where(m.Task.organization_id==user.organization_id)
    if user.role!=m.Role.admin: q=q.where((m.Task.assigned_to==user.id)|(m.Task.assigned_role==user.role))
    return db.scalars(q.order_by(m.Task.due_at)).all()
@app.post(A+"/tasks/{task_id}/approve",response_model=s.TaskOut)
def approve(task_id:str,data:s.Decision,user:m.User=Depends(current_user),db:Session=Depends(get_db)): return services.decide(db,user,task_id,m.TaskStatus.approved,data.comment)
@app.post(A+"/tasks/{task_id}/reject",response_model=s.TaskOut)
def reject(task_id:str,data:s.Decision,user:m.User=Depends(current_user),db:Session=Depends(get_db)): return services.decide(db,user,task_id,m.TaskStatus.rejected,data.comment)
@app.get(A+"/audit-logs",response_model=list[s.AuditOut])
def logs(user:m.User=Depends(require(m.Role.admin,m.Role.manager)),db:Session=Depends(get_db)): return db.scalars(select(m.AuditLog).where(m.AuditLog.organization_id==user.organization_id).order_by(m.AuditLog.created_at.desc()).limit(100)).all()
@app.get(A+"/analytics/overview")
def overview(user:m.User=Depends(current_user),db:Session=Depends(get_db)):
    services.mark_overdue(db,user.organization_id)
    rows=dict(db.execute(select(m.WorkflowExecution.status,func.count()).where(m.WorkflowExecution.organization_id==user.organization_id).group_by(m.WorkflowExecution.status)).all()); overdue=db.scalar(select(func.count()).select_from(m.Task).where(m.Task.organization_id==user.organization_id,m.Task.status==m.TaskStatus.overdue)) or 0
    return {"open":rows.get(m.ExecutionStatus.in_progress,0),"completed":rows.get(m.ExecutionStatus.completed,0),"rejected":rows.get(m.ExecutionStatus.rejected,0),"overdue":overdue}
