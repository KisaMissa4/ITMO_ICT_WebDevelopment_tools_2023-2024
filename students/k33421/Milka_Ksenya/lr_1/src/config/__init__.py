from .database import Database

__all__ = [
    "database_settings",
]

database_settings = Database()  # type: ignore
