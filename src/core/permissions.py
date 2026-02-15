from enum import StrEnum


class PermissionEnum(StrEnum):
    CREATE_USER = "create_user"
    DELETE_USER = "delete_user"
    UPDATE_USER = "update_user"
    CREATE_ROLE = "create_role"
    DELETE_ROLE = "delete_role"
    UPDATE_ROLE = "update_role"
    VIEW_ROLE = "view_role"
