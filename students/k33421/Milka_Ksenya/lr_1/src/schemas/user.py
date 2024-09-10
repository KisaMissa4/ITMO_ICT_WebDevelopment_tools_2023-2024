import typing as tp

from pydantic import BaseModel

from .project import Project
from .skill import UserSkill


class User(BaseModel):
    id: int
    username: str
    first_name: tp.Optional[str]
    last_name: tp.Optional[str]
    email: tp.Optional[str]
    about: tp.Optional[str]


class UserMe(User):
    created_projects: list[Project]
    skills: list[UserSkill]


class UserMember(User):
    role: str
