from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from .models import Question

def index(request):
	latest_question_list = Question.objects.order_by('-pub_date')[:5]
	output = ','.join([q.question_text for q in latest_question_list])
	return HttpResponse(output)


def first(request):
	return HttpResponse("The first poll")

def second(request):
	return HttpResponse("The second url")

def detail(request, question_id):
	return HttpResponse("You're looking at Question %s." %question_id)

def results(request, question_id):
    return HttpResponse("Response %s" % question_id) #Edited from Tutorial.
 
def vote(request, question_id):
	return HttpResponse("You're voting on  question %s." %question_id)
