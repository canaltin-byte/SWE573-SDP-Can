from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from savsha.forms import NewUserForm, EditUserProfileForm, PasswordChangingForm
from savsha.models import Category, Contents
from django.urls import reverse_lazy
from django.views import generic


def first_page(request):
    return render(request, 'main/first_page.html')


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
            return redirect(request.build_absolute_uri('/') + "home/")
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
                return redirect(request.build_absolute_uri('/') + "home/")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="main/login.html", context={"login_form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect(request.build_absolute_uri('/'))


def home(request):
    contents = Contents.objects
    return render(request=request, template_name="main/home.html", context={"contents": contents})


def new_content(request):
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
            return render(request=request, template_name="main/home.html")
        else:
            return render(request=request, template_name="user_page/new_content.html")
    else:
        return render(request=request, template_name="user_page/new_content.html")


def my_profile(request):
    return render(request=request, template_name="user_page/my_profile.html", context={"user": request.user})


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


class PasswordChangeView(PasswordChangeView):
    form_class = PasswordChangingForm
    success_url = reverse_lazy('password_success')


def password_success(request):
    return render(request, "user_page/password_change_success.html")


class UpdateUserView(generic.UpdateView):
    form_class = EditUserProfileForm
    template_name = "user_page/edit_user_profile.html"
    success_url = reverse_lazy("home")

    def get_object(self):
        return self.request.user
