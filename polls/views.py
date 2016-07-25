from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
	return HttpResponse("hello World! You're at the polls index")


def first(request):
	return HttpResponse("The first poll")

def second(request):
	return HttpResponse("The second url")
