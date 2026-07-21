from .accounts import home, profile, register
from .study_resources import books, dictionary, wiki, youtube
from .study_tasks import (
    homework,
    homework_delete,
    homework_toggle,
    note_delete,
    note_detail,
    notes,
    todo,
    todo_delete,
    todo_toggle,
)
from .unit_conversion import conversion


__all__ = [
    "books",
    "conversion",
    "dictionary",
    "home",
    "homework",
    "homework_delete",
    "homework_toggle",
    "note_delete",
    "note_detail",
    "notes",
    "profile",
    "register",
    "todo",
    "todo_delete",
    "todo_toggle",
    "wiki",
    "youtube",
]
