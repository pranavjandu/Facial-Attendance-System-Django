import django_filters
from django_filters import CharFilter
from .models import *
from django import forms

#These filters are used for filtering out the query set in templates according to models

class InstructorFilter(django_filters.FilterSet):
    name=CharFilter(field_name="name",lookup_expr='icontains')
    class Meta:
        model=Instructor
        fields=["name",]

class StudentFilter(django_filters.FilterSet):
    name=CharFilter(field_name="name",lookup_expr='icontains')
    batch_id= django_filters.filters.ModelMultipleChoiceFilter(
        field_name='batch_id',
        queryset=Batch.objects.all(),
        widget=forms.SelectMultiple(attrs={'size':'2'})
    )
    class Meta:
        model=Students
        fields=["name","batch_id"] 

class CourseFilter(django_filters.FilterSet):
    name=CharFilter(field_name="course_name",lookup_expr='icontains')
    class Meta:
        model=Course
        fields=["course_name",]
        exclude=["course_name",]

class BatchFilter(django_filters.FilterSet): 
    name=CharFilter(field_name="batch_name",lookup_expr='icontains')
    class Meta:
        model=Batch
        fields='__all__'
        exclude=['batch_name','days']
    
