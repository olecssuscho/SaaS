from enum import StrEnum

class GlobalRole(StrEnum):
    user = "user"
    admin = "admin"

class TenantRole(StrEnum):
    owner = "owner"
    admin = "admin"
    member = "member"
    viewer = "viewer"