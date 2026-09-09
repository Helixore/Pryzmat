from django.contrib.auth.models import User, Group
from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.permissions import BasePermission
from .models import ConductEntry, StudentClass, Schedule, Teacher, Grade, Student, Subject, Parent
from .lib import validators

class ConductEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = ConductEntry
        fields = ('message', 'type_of_entry', 'points', 'date_of_issue', 'student')
    
    def create(self, validated_data):
        if validated_data.get("student") is None:
            raise ValidationError("Nie można utworzyć uwagi, ponieważ żaden student nie został wybrany.")
        return ConductEntry.objects.create(**validated_data)
        
        
class StudentClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentClass
        fields = ('year', 'symbol')
        
class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ('semester', 'studentClass', 'dateFrom', 'dateTo')
        
class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ('value', 'description', 'date_of_issue', 'student', 'subject')
        
    def create(self, validated_data):
        validators.validate_grade(validated_data.get("value"))
        return Grade.objects.create(**validated_data)

class StudentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    class Meta:
        model = Student
        fields = ('firstName', 'lastName', 'PESEL', 'dateOfBirth', 'parent', 'address', 'studentClass', 'username', 'password')
        
    def create(self, validated_data):
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        pesel = validated_data.get('PESEL', '')
        validators.validate_pesel(pesel)
        student_group = Group.objects.get(name="Student")
        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=validated_data.get('firstName', ''),
            last_name=validated_data.get('lastName', ''),
            email=validated_data.get('email', '')
        )
        user.groups.add(student_group)
        return Student.objects.create(user=user, **validated_data)
    
    def update(self, instance, validated_data):
        username = validated_data.pop('username', None)
        password = validated_data.pop('password', None)

        if 'PESEL' in validated_data:
            validators.validate_pesel(validated_data['PESEL'])

        user = instance.user

        if username:
            user.username = username
        if password:
            user.set_password(password)  # hashuje, w przeciwieństwie do user.password = password
        if username or password:
            user.save()

        # firstName/lastName/email w Meta.fields to pola Teacher,
        # ale trzymasz je zsynchronizowane też na User — więc aktualizuj oba
        if 'firstName' in validated_data:
            user.first_name = validated_data['firstName']
        if 'lastName' in validated_data:
            user.last_name = validated_data['lastName']
        if 'email' in validated_data:
            user.email = validated_data['email']
        if any(k in validated_data for k in ('firstName', 'lastName', 'email')):
            user.save()

        return super().update(instance, validated_data)

class ParentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    class Meta:
        model = Parent
        fields = ('firstName', 'lastName', 'PESEL', 'email', 'address', 'username', 'password')
        
    def create(self, validated_data):
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        pesel = validated_data.get('PESEL', '')
        validators.validate_pesel(pesel)
        parent_group = Group.objects.get(name="Parent")
        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=validated_data.get('firstName', ''),
            last_name=validated_data.get('lastName', ''),
            email=validated_data.get('email', '')
        )
        user.groups.add(parent_group)
        return Parent.objects.create(user=user, **validated_data)
    
    def update(self, instance, validated_data):
        username = validated_data.pop('username', None)
        password = validated_data.pop('password', None)

        if 'PESEL' in validated_data:
            validators.validate_pesel(validated_data['PESEL'])

        user = instance.user

        if username:
            user.username = username
        if password:
            user.set_password(password)  # hashuje, w przeciwieństwie do user.password = password
        if username or password:
            user.save()

        # firstName/lastName/email w Meta.fields to pola Teacher,
        # ale trzymasz je zsynchronizowane też na User — więc aktualizuj oba
        if 'firstName' in validated_data:
            user.first_name = validated_data['firstName']
        if 'lastName' in validated_data:
            user.last_name = validated_data['lastName']
        if 'email' in validated_data:
            user.email = validated_data['email']
        if any(k in validated_data for k in ('firstName', 'lastName', 'email')):
            user.save()

        return super().update(instance, validated_data)

class TeacherSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = Teacher
        fields = ('firstName', 'lastName', 'PESEL', 'address', 'email', 'formTutor', 'username', 'password')
    
    def create(self, validated_data):
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        pesel = validated_data.get('PESEL', '')
        validators.validate_pesel(pesel)
        teacher_group = Group.objects.get(name="Teacher")
        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=validated_data.get('firstName', ''),
            last_name=validated_data.get('lastName', ''),
            email=validated_data.get('email', '')
        )
        user.groups.add(teacher_group)
        return Teacher.objects.create(user=user, **validated_data)
        
    def update(self, instance, validated_data):
        username = validated_data.pop('username', None)
        password = validated_data.pop('password', None)

        if 'PESEL' in validated_data:
            validators.validate_pesel(validated_data['PESEL'])

        user = instance.user

        if username:
            user.username = username
        if password:
            user.set_password(password)  # hashuje, w przeciwieństwie do user.password = password
        if username or password:
            user.save()

        # firstName/lastName/email w Meta.fields to pola Teacher,
        # ale trzymasz je zsynchronizowane też na User — więc aktualizuj oba
        if 'firstName' in validated_data:
            user.first_name = validated_data['firstName']
        if 'lastName' in validated_data:
            user.last_name = validated_data['lastName']
        if 'email' in validated_data:
            user.email = validated_data['email']
        if any(k in validated_data for k in ('firstName', 'lastName', 'email')):
            user.save()

        return super().update(instance, validated_data)

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ('name', 'hours', 'teacher', 'studentClass')