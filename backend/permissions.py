from typing import List, Dict
from enum import Enum, auto


class Permission(Enum):
    CREATE = auto()
    READ = auto()
    UPDATE = auto()
    DELETE = auto()


async def get_app_permissions(app):
    resource_types = await app.mongodb.list_collection_names()

    app.permissions = {
        "admin": {
            resource: list(Permission.__members__.values())
            for resource in resource_types
        },
        "auditor": {resource: [Permission.READ] for resource in resource_types},
        "editor": {
            "users": [],
            "raags": list(Permission.__members__.values()),
            "taals": list(Permission.__members__.values()),
            "compositions": list(Permission.__members__.values()),
        },
        "reader": {
            "users": [],
            "raags": [Permission.READ],
            "taals": [Permission.READ],
            "compositions": [Permission.READ],
        },
    }


def get_permission_names(permissions: List[Permission]):
    return [perm.name for perm in permissions]


def permission_check(
    permissions: Dict, user: Dict, record: Dict, collection: str, operation: str
) -> bool:
    role_permissions = [
        perm.name for perm in permissions[user["role"]].get(collection, [])
    ]
    group_permissions = set.union(
        *[
            set(grp.get("permissions", []))
            for grp in filter(
                lambda grp: grp.get("name", "") in user.get("groups", []),
                record["groups"],
            )
        ]
    )

    if any(
        [
            record["owner"] == user["name"],
            operation in role_permissions,
            operation in group_permissions,
        ]
    ):
        return True
    return False


"""
In the following example John is only a reader, but ha can modify or delete
document 'foo', because he is part of group 'boo'.

{
  "users": [{
    "name": "john",
    "display_name": "John Doe",
    "role": "reader",
    "groups": ["boo"]
  }],
  "document": [{
    "name": "foo",
    "owner" "bar",
    "groups": [
      {
        "name": "baz",
        "permissions": ["read"]
      }
      {
        "name": "boo",
        "permissions": ["read", "update", "delete"]
      }
    ]
  }]
}
"""
