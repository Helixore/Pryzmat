from django.db.models import Avg, Count, Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from Pryzmat.models import ConductEntry, Quiz, Lesson, Grade, Student
from Pryzmat.serializers import StudentParentDashboardSerializer, TeacherDashboardSerializer

def resolve_role(user):
    # PLACEHOLDER: adjust if you set related_name on the OneToOne fields
    for role in ("principal", "teacher", "parent", "student"):
        if hasattr(user, role):
            return role, getattr(user, role)
    return None, None

# MOVED: from DashboardView.visible_students
def visible_students(role, profile):
    if role == "principal":
        return Student.objects.all()

    if role == "teacher":
        return Student.objects.filter(
            Q(studentClass__subject__teacher=profile)
            | Q(studentClass__homeroomTeacher=profile)
        ).distinct()

    if role == "parent":
        return Student.objects.filter(parent=profile)

    if role == "student":
        return Student.objects.filter(pk=profile.pk)

    return Student.objects.none() 

class DashboardView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_classes = {
        "teacher": TeacherDashboardSerializer,
        "parent": StudentParentDashboardSerializer,
        "student": StudentParentDashboardSerializer,
    }
    def get(self, request):
        role, profile = resolve_role(request.user)

        serializer_class = self.serializer_classes.get(role)
        if serializer_class is None:
            return Response({"detail": "No dashboard for this account."}, status=403)

        # one build_<role>_data method per role
        builder = getattr(self, f"build_{role}_data")
        data = builder(profile)

        serializer = serializer_class(data)
        return Response(serializer.data)
    
    def build_teacher_data(self, teacher):
        # query whatever teachers need, return a dict
        return {...}

    def build_parent_data(self, parent):
        students = Student.objects.filter(student__parent=parent)
        return self.build_student_data(self, students)

    def build_student_data(self, student):
        quizes = Quiz.objects.filter(lesson__schedule__studentClass__student=student).order_by("-timestamp")
        quizes_items = []
        for quiz in quizes[:5]:
            quizes_items.append({
                "type": quiz.type,
                "quiz": quiz
            })
        lessons = Lesson.objects.filter(schedule__studentClass__student=student).select_related("subject").order_by("-dateTimeFrom")
        lesson_items = (
            lessons[:5]
        )
        grades = Grade.objects.filter(student=student)
        total = 0.0
        for grade in grades:
            if grade.value is not None:  # skip grades whose property returns None
                total += grade.value
        total = total / grades.count()
        quizes_dict = {}
        lessons_dict = {}
        grades_dict = {}
        if not quizes_items:
            quizes_dict = None
        else:
            quizes_dict = {
                "type": [x.keys() for x in quizes_items],
                "quizes": [x.values() for x in quizes_items]
            }
        if not lesson_items:
            lessons_dict = None
        else:
            lessons_dict = {
                "total": lesson_items.count(),
                "lessons": lesson_items
            }
        if not grades:
            grades_dict = None
        else:
            print(total)
            grades_dict = {
                "total": grades.count(),
                "average": total #average_grades_by_subjects
            }
        return {
            "quizes": quizes_dict,
            "lessons": lessons_dict,
            "grades": grades_dict
        }