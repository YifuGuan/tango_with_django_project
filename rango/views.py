from datetime import datetime
from logging.config import valid_ident
from urllib import response
from django.urls import reverse
from django import http
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
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

    visitor_cookie_handler(request)

    response = render(request, 'rango/index.html', context=context_dict)

    # render the response and send it back
    return response


def about(request):
    context_dict = {
        'boldmessage': 'This tutorial has been put together by Yifu.'}
    
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']

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
    if not request.user.is_authenticated:
        return redirect(reverse('rango:login'))
    else:
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
    if not request.user.is_authenticated:
        return redirect(reverse('rango:login'))
    else:
        return render(request, 'rango/add_page.html', context=context_dict)
    

def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            # save user's data to database
            user = user_form.save()

            # hash the password
            user.set_password(user.password)

            # then update the user object
            user.save()

            # sort out userprofile instances
            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        # not a HTTP POST
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,
                'rango/register.html',
                context = {'user_form': user_form,
                           'profile_form': profile_form,
                           'registered': registered})

def user_login(request):
    if request.method == 'POST':
        # get username and password inputs
        username = request.POST.get('username')
        password = request.POST.get('password')

        # invalid check
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('rango:index'))
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    
    else:
        # HTTP GET in most occasion
        return render(request, 'rango/login.html')

def restricted(request): 
    if not request.user.is_authenticated:
        return redirect(reverse('rango:login'))
    else:
        return render(request, 'rango/restricted.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('rango:index'))

def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

def visitor_cookie_handler(request):
    # count visitors
    # get cookies, once no cookies found, pass second paramater as default 
    visits = int(get_server_side_cookie(request, 'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],
                                        '%Y-%m-%d %H:%M:%S')
    
    # one day since last visited
    if(datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        # update cookie: last_visit
        request.session['last_visit'] = str(datetime.now())
    else:
        # set last cookie
        request.session['last_visit'] = last_visit_cookie
    
    # update cookie: visit times
    request.session['visits'] = visits
