import imp
from multiprocessing import context
from django import http
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def index(request):
    context_dict = {'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!'}
    return render(request, 'rango/index.html', context=context_dict)


def about(request):
    context_dict = {
        'boldmessage': 'This tutorial has been put together by Yifu.'}
    return render(request, 'rango/about.html', context=context_dict)
