from datetime import datetime
from sqlalchemy.orm import mapped_column, DeclarativeBase, Mapped
from typing import Annotated
from sqlalchemy import String, text


str_255 = Annotated[str, mapped_column(String(255), nullable=True)]
str_255_unique = Annotated[str, mapped_column(String(255), nullable=False, unique=True)]
bool_default_true = Annotated[bool, mapped_column(default=True)]
bool_default_false = Annotated[bool, mapped_column(default=False)]
created_at = Annotated[
    datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))
]


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
