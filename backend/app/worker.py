from celery import Celery
from sqlalchemy import select
from datetime import datetime,timezone
from .config import settings
from .database import SessionLocal
from .models import Task,TaskStatus
celery=Celery("opsflow",broker=settings.redis_url,backend=settings.redis_url)
@celery.task(name="app.worker.mark_overdue")
def mark_overdue():
    with SessionLocal() as db:
        tasks=db.scalars(select(Task).where(Task.status==TaskStatus.pending,Task.due_at<datetime.now(timezone.utc))).all()
        for task in tasks: task.status=TaskStatus.overdue
        db.commit(); return len(tasks)
