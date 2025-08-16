from pydantic import BaseModel


class BaseRoleSchema(BaseModel):
    name: str


class RoleCreateSchema(BaseRoleSchema):
    pass


class RoleResponseSchema(BaseRoleSchema):
    id: int
    name: str


class RoleListSchema(BaseModel):
    roles: list[RoleResponseSchema]
    count_of_pages: int
    count_of_roles: int


class RoleFilter(BaseModel):
    id__in: list[str] | None = None
    name__like: str | None = None
