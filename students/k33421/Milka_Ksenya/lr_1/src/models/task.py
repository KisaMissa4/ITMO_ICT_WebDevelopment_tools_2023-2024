import typing as tp
from datetime import datetime

from sqlmodel import Field, Relationship, SQLModel

from . import mixins

if tp.TYPE_CHECKING:
    from .project import Project
    from .user import User


class Task(mixins.IDMixin, SQLModel, table=True):
    name: str
    description: tp.Optional[str] = None
    status: str
    due_date: tp.Optional[datetime] = None
    project_id: tp.Optional[int] = Field(None, foreign_key="project.id")
    creator_id: tp.Optional[int] = Field(None, foreign_key="user.id")
    assignee_id: tp.Optional[int] = Field(None, foreign_key="user.id")

    creator: "User" = Relationship(
        back_populates="created_tasks",
        sa_relationship_kwargs={"foreign_keys": "[Task.creator_id]"}
    )
    assignee: "User" = Relationship(
        back_populates="assigned_tasks",
        sa_relationship_kwargs={"foreign_keys": "[Task.assignee_id]"}
    )
    project: "Project" = Relationship(back_populates="tasks")
