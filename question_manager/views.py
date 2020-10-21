from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse('Hello from manager!')


def get_all_categories(request):
    pass


def create_category(request):
    pass


def remove_category(request):
    pass


def change_category(request):
    pass


def get_all_questions(request):
    pass


def create_question(request):
    pass


def remove_question(request):
    pass


def change_question(request):
    pass
