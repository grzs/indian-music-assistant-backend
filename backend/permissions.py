from typing import Dict
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


def permission_check(
    app_permissions: Dict,
    requested_permission: Permission,
    user: Dict,
    record: Dict,
    collection: str,
) -> bool:
    """Returns true if:
    - the user is the owner of the record
    - the user is a member of a role that has the requested permission over the records collection
    - the user is a member of a group that has been granted the requested permission on the record
    """

    role_permissions = app_permissions[user["role"]].get(collection, [])
    if record["owner"] == user["name"] or requested_permission in role_permissions:
        return True

    # checking group permissions
    for group_permission in record["group_permissions"]:
        if group_permission.get("group", "") not in user.get("groups", []):
            continue
        for permission_name in group_permission["permissions"]:
            try:
                if Permission[permission_name.upper()] == requested_permission:
                    return True
            except KeyError as e:
                print(e)  # TODO: log instead of print

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
    "group_permissions": [
      {
        "group": "baz",
        "permissions": ["read"]
      }
      {
        "group": "boo",
        "permissions": ["read", "update", "delete"]
      }
    ]
  }]
}
"""
