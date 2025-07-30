from __future__ import annotations

from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.orm.base import (
    Base,
    str_255,
    str_255_unique,
    bool_default_false,
    bool_default_true,
)


class User(Base):
    __tablename__ = "users"

    email: Mapped[str_255_unique]
    password: Mapped[str_255]
    first_name: Mapped[str_255]
    last_name: Mapped[str_255]
    is_superuser: Mapped[bool_default_false]
    is_active: Mapped[bool_default_true]

    role_id: Mapped[int | None] = mapped_column(ForeignKey("roles.id"))
    role: Mapped[Optional["Role"]] = relationship(back_populates="users")
