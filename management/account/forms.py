from django.forms import ModelForm
from .models import Students,Batch
from django import forms

class AddStudentForm(forms.Form):
    username=forms.CharField(label="Username",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    email=forms.EmailField(label="Email",max_length=50,widget=forms.EmailInput(attrs={"class":"form-control"}))
    password=forms.CharField(label="Password",max_length=50,widget=forms.PasswordInput(attrs={"class":"form-control"}))
    first_name=forms.CharField(label="First Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name=forms.CharField(label="Last Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))

    batches=Batch.objects.all() 
    batch_list=[]
    for batch in batches:
        small_batch=(batch.id,batch.batch_name)
        batch_list.append(small_batch)

    batch1=forms.ChoiceField(label="Batch",choices=batch_list,widget=forms.Select(attrs={"class":"form-control"}))