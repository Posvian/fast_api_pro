from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Mapped, relationship

from src.permissions.models.permissions import PermissionRoleAssociation

from src.core.orm.base import (
    Base,
    str_255_unique,
)


class Role(Base):
    __tablename__ = "roles"

    name: Mapped[str_255_unique]
    users: Mapped[Optional[list["User"]]] = relationship(back_populates="role")
    permission_associations: Mapped[Optional["PermissionRoleAssociation"]] = (
        relationship(back_populates="role")
    )
