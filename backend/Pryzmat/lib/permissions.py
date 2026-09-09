from rest_framework.permissions import BasePermission, SAFE_METHODS


def user_group(user):
    """Zwraca nazwę pierwszej dopasowanej grupy usera, albo None."""
    group_names = set(user.groups.values_list('name', flat=True))
    for name in ('Principal', 'Teacher', 'Parent', 'Student'):
        if name in group_names:
            return name
    return None


class IsTeacherOrPrincipal(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:  # GET, HEAD, OPTIONS
            return True  # odczyt kontrolowany przez get_queryset
        group = user_group(request.user)
        return group in ('Teacher', 'Principal')