"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views as ATViews
from rest_framework import routers
from Pryzmat import views
from Pryzmat.lib import PryzmatAuthToken

router = routers.DefaultRouter()
router.register(r'conductentries', views.conductEntry.ConductEntryView, 'conductentry') #git
router.register(r'studentclass', views.studentClass.StudentClassView, 'studentclass') #git
router.register(r'schedule', views.schedule.ScheduleView, 'schedule') #git
router.register(r'teacher', views.teacher.TeacherView, 'teacher') #git
router.register(r'grade', views.grade.GradeView, 'grade') #git
router.register(r'student', views.student.StudentView, 'student') #git
router.register(r'parent', views.parent.ParentView, 'parent') #git
router.register(r'subject', views.subject.SubjectView, 'subject') #git
router.register(r'lesson', views.lesson.LessonView, 'lesson') #git
router.register(r'message', views.message.MessageView, 'message')
router.register(r'presence', views.presence.PresenceView, 'presence')
router.register(r'substitution', views.substitution.SubstitutionView, 'substitution')
router.register(r'principal', views.principal.PrincipalView, 'principal')
router.register(r'worker', views.worker.WorkerView, 'worker')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth', include('rest_framework.urls')),
    path('api/', include(router.urls)),
    path('api/login', PryzmatAuthToken.PryzmatAuthToken.as_view())
]
