import typing as tp

from sqlmodel import Field, Relationship, SQLModel

from . import mixins

if tp.TYPE_CHECKING:
    from .user_skill import UserSkill
    from .project import Project
    from .project_user import ProjectUser


class User(mixins.IDMixin, SQLModel, table=True):
    username: str = Field(index=True)
    password: str
    first_name: tp.Optional[str] = None
    last_name: tp.Optional[str] = None
    email: tp.Optional[str] = None

    user_skills: list["UserSkill"] = Relationship(back_populates="users")
    created_projects: list["Project"] = Relationship(back_populates="creator")
    members: list["ProjectUser"] = Relationship(back_populates="user")
