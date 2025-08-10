from pydantic import BaseModel


class BaseRoleSchema(BaseModel):
    name: str


class RoleCreateSchema(BaseRoleSchema):
    pass


class RoleResponseSchema(BaseRoleSchema):
    id: int
    name: str
