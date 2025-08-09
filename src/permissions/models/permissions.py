from __future__ import annotations

from typing import Optional

from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from src.core.orm.base import (
    Base,
    str_255,
)


class PermissionRoleAssociation(Base):
    __tablename__ = "permission_role_association_table"  # исправить название
    permission_id: Mapped[int] = mapped_column(
        ForeignKey("permissions.id"), primary_key=True
    )
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), primary_key=True)
    permission: Mapped["Permissions"] = relationship(back_populates="role_associations")
    role: Mapped["Role"] = relationship(back_populates="permission_associations")


class Permissions(Base):
    __tablename__ = "permissions"

    name: Mapped[str_255]
    role_associations: Mapped[Optional["PermissionRoleAssociation"]] = relationship(
        back_populates="permission"
    )
