from .permissions import user_group

class RoleFilteredQuerysetMixin:
    """
    Wymaga, żeby ViewSet zdefiniował:
    - queryset (pełny, dla dyrka)
    - filter_for_teacher(self, qs, teacher)
    - filter_for_parent(self, qs, parent)
    - filter_for_student(self, qs, student)
    """
    def get_queryset(self):
        user = self.request.user
        group = user_group(user)
        base_qs = self.queryset

        if group == 'Principal':
            return base_qs
        if group == 'Teacher':
            return self.filter_for_teacher(base_qs, user.teacher)
        if group == 'Parent':
            return self.filter_for_parent(base_qs, user.parent)
        if group == 'Student':
            return self.filter_for_student(base_qs, user.student)
        return base_qs.none()  # brak grupy = domyślnie nic nie widzi