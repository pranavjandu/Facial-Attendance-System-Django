from django.shortcuts import render,HttpResponse

# Create your views here.

def loginpage(request):
    return HttpResponse("Hi")