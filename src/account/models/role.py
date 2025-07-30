from __future__ import annotations
from sqlalchemy.orm import Mapped, relationship


from src.core.orm.base import (
    Base,
    str_255,
)


class Role(Base):
    __tablename__ = "roles"

    name: Mapped[str_255]
    users: Mapped[list["User"]] = relationship(back_populates="role")
