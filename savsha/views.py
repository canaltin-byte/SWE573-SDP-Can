from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from savsha.forms import NewUserForm
from savsha.models import Category, Contents


def list(request):
    return render(request, 'main/list.html')


def test(request):
    form = NewUserForm()
    return render(request=request, template_name='main/test.html', context={"form": form})


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("http://127.0.0.1:8000/home/")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="main/register.html", context={"form": form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("http://127.0.0.1:8000/home/")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="main/login.html", context={"login_form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("http://127.0.0.1:8000/")


def home(request):
    return render(request=request, template_name="main/home.html")


def new_content(request):
    content = Contents.objects
    if request.method == 'POST':
        if request.POST.get('title') and request.POST.get('message') and request.POST.get('address') \
                and request.POST.get('labels'):
            c = Contents()
            c.user_id = request.user.id
            c.title = request.POST.get('title')
            c.message = request.POST.get('message')
            c.address = request.POST.get('address')
            c.labels = request.POST.get('labels')
            c.save()
            return render(request=request, template_name="main/home.html", context={"categories": content})
    else:
        return render(request=request, template_name="user_page/new_content.html", context={"categories": content})
    return render(request=request, template_name="user_page/new_content.html")


def category(request):
    categories = Category.objects
    if request.method == 'POST':
        if request.POST.get('user') and request.POST.get('category'):
            c = Category()
            c.user_id = request.POST.get('user')
            c.category_names = request.POST.get('category')
            c.save()
            return render(request=request, template_name="user_page/category.html", context={"categories": categories})
    else:
        return render(request=request, template_name="user_page/category.html", context={"categories": categories})
