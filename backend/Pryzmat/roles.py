ALL_ROLES = ["student", "teacher", "parent", "principal", "worker"]


def get_roles(user):
    """Return a list of role names that this user has."""
    roles = []
    for role in ALL_ROLES:
        if hasattr(user, role):
            roles.append(role)
    return roles