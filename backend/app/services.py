import re
from datetime import datetime,timedelta,timezone
from fastapi import HTTPException
from sqlalchemy import func,select
from sqlalchemy.orm import Session
from . import models as m
from .security import hash_password,verify_password
def audit(db,user,action,entity,entity_id,details=None): db.add(m.AuditLog(organization_id=user.organization_id,user_id=user.id,action=action,entity=entity,entity_id=entity_id,details=details or {}))
def register(db:Session,data):
    if db.scalar(select(m.User).where(func.lower(m.User.email)==data.email.lower())): raise HTTPException(409,"E-mail já cadastrado")
    base=re.sub(r"[^a-z0-9]+","-",data.organization_name.lower()).strip("-") or "empresa"; slug=base; n=1
    while db.scalar(select(m.Organization).where(m.Organization.slug==slug)): n+=1; slug=f"{base}-{n}"
    org=m.Organization(name=data.organization_name,slug=slug); db.add(org); db.flush()
    user=m.User(organization_id=org.id,name=data.name,email=data.email.lower(),password_hash=hash_password(data.password),role=m.Role.admin); db.add(user); db.flush(); audit(db,user,"created","organization",org.id); db.commit(); return user
def authenticate(db,email,password):
    user=db.scalar(select(m.User).where(func.lower(m.User.email)==email.lower()))
    if not user or not verify_password(password,user.password_hash): raise HTTPException(401,"E-mail ou senha inválidos")
    return user
def tenant(db,model,user,obj_id):
    obj=db.scalar(select(model).where(model.id==obj_id,model.organization_id==user.organization_id))
    if not obj: raise HTTPException(404,"Recurso não encontrado")
    return obj
def create_task(db,org_id,execution_id,step):
    assignee=db.scalar(select(m.User).where(m.User.organization_id==org_id,m.User.role==step.assigned_role,m.User.active.is_(True)).order_by(m.User.created_at))
    task=m.Task(organization_id=org_id,execution_id=execution_id,workflow_step_id=step.id,assigned_to=assignee.id if assignee else None,assigned_role=step.assigned_role,due_at=datetime.now(timezone.utc)+timedelta(hours=step.sla_hours)); db.add(task)
def mark_overdue(db:Session,organization_id:str):
    tasks=db.scalars(select(m.Task).where(m.Task.organization_id==organization_id,m.Task.status==m.TaskStatus.pending,m.Task.due_at<datetime.now(timezone.utc))).all()
    for task in tasks: task.status=m.TaskStatus.overdue
    if tasks: db.commit()
def start_execution(db,user,data):
    workflow=tenant(db,m.Workflow,user,data.workflow_id)
    if workflow.status!=m.WorkflowStatus.active: raise HTTPException(409,"Somente workflows ativos podem ser executados")
    if not workflow.steps: raise HTTPException(409,"Workflow não possui etapas")
    execution=m.WorkflowExecution(organization_id=user.organization_id,workflow_id=workflow.id,started_by=user.id,request_data=data.request_data); db.add(execution); db.flush(); create_task(db,user.organization_id,execution.id,workflow.steps[0]); audit(db,user,"started","execution",execution.id); db.commit(); return execution
def decide(db,user,task_id,status,comment):
    task=tenant(db,m.Task,user,task_id)
    if task.status not in (m.TaskStatus.pending,m.TaskStatus.overdue): raise HTTPException(409,"Tarefa já decidida")
    execution=tenant(db,m.WorkflowExecution,user,task.execution_id)
    if execution.started_by==user.id: raise HTTPException(409,"O solicitante não pode aprovar a própria solicitação")
    if user.role!=task.assigned_role and user.role!=m.Role.admin: raise HTTPException(403,"Tarefa atribuída a outro perfil")
    task.status=status; task.completed_at=datetime.now(timezone.utc); db.add(m.Approval(task_id=task.id,user_id=user.id,status=status,comment=comment))
    if status==m.TaskStatus.rejected: execution.status=m.ExecutionStatus.rejected; execution.completed_at=datetime.now(timezone.utc)
    else:
        step=db.get(m.WorkflowStep,task.workflow_step_id); next_step=db.scalar(select(m.WorkflowStep).where(m.WorkflowStep.workflow_id==execution.workflow_id,m.WorkflowStep.order>step.order).order_by(m.WorkflowStep.order))
        if next_step: create_task(db,user.organization_id,execution.id,next_step)
        else: execution.status=m.ExecutionStatus.completed; execution.completed_at=datetime.now(timezone.utc)
    audit(db,user,status.value,"task",task.id,{"comment":comment}); db.commit(); return task
