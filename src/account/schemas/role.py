from pydantic import BaseModel


class BaseRoleSchema(BaseModel):
    name: str


class RoleCreateSchema(BaseRoleSchema):
    pass


class RoleListSchema(BaseRoleSchema):
    id: int
    name: str
