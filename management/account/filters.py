import django_filters
from django_filters import CharFilter
from .models import *

class InstructorFilter(django_filters.FilterSet):
    name=CharFilter(field_name="name",lookup_expr='icontains')
    class Meta:
        model=Instructor
        fields=["name",]

class StudentFilter(django_filters.FilterSet):
    name=CharFilter(field_name="name",lookup_expr='icontains')
    class Meta:
        model=Students
        fields=["name",]

class CourseFilter(django_filters.FilterSet):
    name=CharFilter(field_name="course_name",lookup_expr='icontains')
    class Meta:
        model=Course
        fields=["course_name",]
        exclude=["course_name",]
    
