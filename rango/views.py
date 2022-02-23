from django.urls import reverse
from pydoc import pager
from django import http
from django.shortcuts import redirect, render
from django.http import HttpResponse
from rango.forms import CategoryForm, PageForm
from rango.models import Category
from rango.models import Page

# Create your views here.


def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]

    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    context_dict['pages'] = page_list

    # render the response and send it back
    return render(request, 'rango/index.html', context=context_dict)


def about(request):
    context_dict = {
        'boldmessage': 'This tutorial has been put together by Yifu.'}
    return render(request, 'rango/about.html', context=context_dict)


def show_category(request, category_name_slug):
    context_dict = {}

    try:
        # get a category object according to slug name of a category
        category = Category.objects.get(slug=category_name_slug)

        # get a list of pages under a specific category
        pages = Page.objects.filter(category=category)

        context_dict['pages'] = pages
        context_dict['category'] = category

    except Category.DoesNotExist:
        context_dict['pages'] = None
        context_dict['category'] = None

    return render(request, 'rango/category.html', context=context_dict)


def add_category(request):
    form = CategoryForm()

    # check HTTP post
    # POST: different with GET, when submitting data from client's browser,
    # POST request which contains a form will be sent.
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # validation check
        if form.is_valid():
            # save the form to database
            form.save(commit=True)
            # redirect to index view
            return redirect('/rango/')
        else:
            print(form.errors)

    # rander the form and get a add_category html file
    return render(request, 'rango/add_category.html', {'form': form})


def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    # back to index page once there is no page in category
    if category is None:
        return redirect('/rango/')

    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()

                # redirect to show_category view
                return redirect(reverse('rango:show_category',
                                        kwargs={'category_name_slug': category_name_slug}))

        else:
            print(form.errors)

    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context=context_dict)
