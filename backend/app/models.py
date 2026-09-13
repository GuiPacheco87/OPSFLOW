import enum,uuid
from datetime import datetime,timezone
from sqlalchemy import Boolean,DateTime,Enum,ForeignKey,Integer,JSON,String,Text,UniqueConstraint
from sqlalchemy.orm import Mapped,mapped_column,relationship
from .database import Base
def uid(): return str(uuid.uuid4())
def now(): return datetime.now(timezone.utc)
class Role(str,enum.Enum): admin="admin"; manager="manager"; member="member"
class WorkflowStatus(str,enum.Enum): draft="draft"; active="active"; inactive="inactive"
class ExecutionStatus(str,enum.Enum): in_progress="in_progress"; completed="completed"; rejected="rejected"
class TaskStatus(str,enum.Enum): pending="pending"; approved="approved"; rejected="rejected"; overdue="overdue"
class Organization(Base):
    __tablename__="organizations"
    id:Mapped[str]=mapped_column(String(36),primary_key=True,default=uid); name:Mapped[str]=mapped_column(String(120)); slug:Mapped[str]=mapped_column(String(80),unique=True); created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now)
class User(Base):
    __tablename__="users"; __table_args__=(UniqueConstraint("organization_id","email"),)
    id:Mapped[str]=mapped_column(String(36),primary_key=True,default=uid); organization_id:Mapped[str]=mapped_column(ForeignKey("organizations.id"),index=True); name:Mapped[str]=mapped_column(String(120)); email:Mapped[str]=mapped_column(String(255),index=True); password_hash:Mapped[str]=mapped_column(String(255)); role:Mapped[Role]=mapped_column(Enum(Role),default=Role.member); active:Mapped[bool]=mapped_column(Boolean,default=True); created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now)
class Workflow(Base):
    __tablename__="workflows"
    id:Mapped[str]=mapped_column(String(36),primary_key=True,default=uid); organization_id:Mapped[str]=mapped_column(ForeignKey("organizations.id"),index=True); name:Mapped[str]=mapped_column(String(160)); description:Mapped[str]=mapped_column(Text,default=""); status:Mapped[WorkflowStatus]=mapped_column(Enum(WorkflowStatus),default=WorkflowStatus.draft); created_by:Mapped[str]=mapped_column(ForeignKey("users.id")); created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now); steps:Mapped[list["WorkflowStep"]]=relationship(cascade="all, delete-orphan",order_by="WorkflowStep.order")
class WorkflowStep(Base):
    __tablename__="workflow_steps"; __table_args__=(UniqueConstraint("workflow_id","order"),)
    id:Mapped[str]=mapped_column(String(36),primary_key=True,default=uid); workflow_id:Mapped[str]=mapped_column(ForeignKey("workflows.id",ondelete="CASCADE"),index=True); name:Mapped[str]=mapped_column(String(160)); order:Mapped[int]=mapped_column(Integer); assigned_role:Mapped[Role]=mapped_column(Enum(Role),default=Role.manager); action_type:Mapped[str]=mapped_column(String(40),default="approval"); required:Mapped[bool]=mapped_column(Boolean,default=True); sla_hours:Mapped[int]=mapped_column(Integer,default=24)
class WorkflowExecution(Base):
    __tablename__="workflow_executions"
    id:Mapped[str]=mapped_column(String(36),primary_key=True,default=uid); organization_id:Mapped[str]=mapped_column(ForeignKey("organizations.id"),index=True); workflow_id:Mapped[str]=mapped_column(ForeignKey("workflows.id")); started_by:Mapped[str]=mapped_column(ForeignKey("users.id")); status:Mapped[ExecutionStatus]=mapped_column(Enum(ExecutionStatus),default=ExecutionStatus.in_progress); request_data:Mapped[dict]=mapped_column(JSON,default=dict); started_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now); completed_at:Mapped[datetime|None]=mapped_column(DateTime(timezone=True),nullable=True)
class Task(Base):
    __tablename__="tasks"
    id:Mapped[str]=mapped_column(String(36),primary_key=True,default=uid); organization_id:Mapped[str]=mapped_column(ForeignKey("organizations.id"),index=True); execution_id:Mapped[str]=mapped_column(ForeignKey("workflow_executions.id")); workflow_step_id:Mapped[str]=mapped_column(ForeignKey("workflow_steps.id")); assigned_to:Mapped[str|None]=mapped_column(ForeignKey("users.id"),nullable=True); assigned_role:Mapped[Role]=mapped_column(Enum(Role)); status:Mapped[TaskStatus]=mapped_column(Enum(TaskStatus),default=TaskStatus.pending); due_at:Mapped[datetime]=mapped_column(DateTime(timezone=True)); completed_at:Mapped[datetime|None]=mapped_column(DateTime(timezone=True),nullable=True)
class Approval(Base):
    __tablename__="approvals"
    id:Mapped[str]=mapped_column(String(36),primary_key=True,default=uid); task_id:Mapped[str]=mapped_column(ForeignKey("tasks.id")); user_id:Mapped[str]=mapped_column(ForeignKey("users.id")); status:Mapped[TaskStatus]=mapped_column(Enum(TaskStatus)); comment:Mapped[str]=mapped_column(Text,default=""); created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now)
class AuditLog(Base):
    __tablename__="audit_logs"
    id:Mapped[str]=mapped_column(String(36),primary_key=True,default=uid); organization_id:Mapped[str]=mapped_column(ForeignKey("organizations.id"),index=True); user_id:Mapped[str]=mapped_column(ForeignKey("users.id")); action:Mapped[str]=mapped_column(String(80)); entity:Mapped[str]=mapped_column(String(80)); entity_id:Mapped[str]=mapped_column(String(36)); details:Mapped[dict]=mapped_column(JSON,default=dict); created_at:Mapped[datetime]=mapped_column(DateTime(timezone=True),default=now)
