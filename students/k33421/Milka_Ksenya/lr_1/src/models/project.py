import typing as tp
from datetime import datetime

from sqlmodel import Field, Relationship, SQLModel

from . import mixins

if tp.TYPE_CHECKING:
    from .user import User
    from .project_user import ProjectUser


class Project(mixins.IDMixin, SQLModel, table=True):
    title: str
    description: tp.Optional[str]
    is_active: bool = False
    start_date: datetime
    end_date: tp.Optional[datetime]
    creator_id: tp.Optional[int] = Field(None, foreign_key="user.id")

    creator: "User" = Relationship(back_populates="created_projects")
    members: list["ProjectUser"] = Relationship(back_populates="project")
