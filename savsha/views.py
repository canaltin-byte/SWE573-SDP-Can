from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from savsha.forms import NewUserForm, EditUserProfileForm, PasswordChangingForm
from savsha.models import Contents, Friends, Likes, Comments, ExtendedUser
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import get_user_model
from django.db.models import Q


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
    return redirect(request.build_absolute_uri('/'))


def home(request):
    contents = Contents.objects.all().order_by("-id").filter(private=False)
    if request.method == 'POST':
        if request.POST.get('search'):
            searched_text = request.POST.get('search')
            contents = contents.filter(Q(title__icontains=searched_text) | Q(message__icontains=searched_text) | Q(
                labels__contains=searched_text))
            return render(request=request, template_name="main/home.html", context={"contents": contents})
        if request.POST.get('methods'):
            method = request.POST.get('methods')
            if method == 'all':
                return render(request=request, template_name="main/home.html", context={"contents": contents})
            if method == 'saving':
                savings = Contents.objects.all().order_by("-id").filter(Q(user_id=request.user.id))
                return render(request=request, template_name="main/home.html", context={"contents": savings})
            if method == 'space':
                my_friends_ids = Friends.objects.all().filter(user_id=request.user.id).values_list('friend_ids',
                                                                                                   flat=True)
                space = contents.filter(Q(user_id=my_friends_ids[0]))
                for l in range(len(my_friends_ids) - 1):
                    space = space | contents.filter(Q(user_id=my_friends_ids[l + 1]))
                return render(request=request, template_name="main/home.html", context={"contents": space})
        if request.POST.get('extend'):
            content_id = request.POST.get('extend')
            likes = Likes.objects.all().filter(content_id=content_id)
            comments = Comments.objects.all().filter(content_id=content_id)
            content = contents.filter(id=content_id)
            return render(request=request, template_name="main/content_detail.html", context={"contents": content, "likes": likes, "comments": comments})
        if request.POST.get('content_like'):
            liked_check = Likes.objects.all().filter(Q(user_id=request.user.id) & Q(content_id=request.POST['content_like']))
            if not liked_check:
                l = Likes()
                l.content_id = request.POST['content_like']
                l.user_id = request.user.id
                l.save()
            content = contents.filter(id=request.POST['content_like'])
            likes = Likes.objects.all().filter(content_id=request.POST['content_like'])
            comments = Comments.objects.all().filter(content_id=request.POST['content_like'])
            return render(request=request, template_name="main/content_detail.html", context={"contents": content, "likes": likes, "comments": comments})
        if request.POST.get('new_comment'):
            content = contents.filter(id=request.POST['content_idc'])
            likes = Likes.objects.all().filter(content_id=request.POST['content_idc'])
            new_comment = request.POST.get('new_comment')
            c = Comments()
            c.content_id = request.POST['content_idc']
            c.user_id = request.user.id
            c.first_name = request.user.first_name
            c.last_name = request.user.last_name
            c.comment = new_comment
            c.save()
            comments = Comments.objects.all().filter(Q(user_id=request.user.id) & Q(content_id=request.POST['content_idc']))
            return render(request=request, template_name="main/content_detail.html",
                          context={"contents": content, "likes": likes, "comments": comments})
    return render(request=request, template_name="main/home.html", context={"contents": contents})


def new_content(request):
    if request.method == 'POST':
        if request.POST.get('title') and request.POST.get('message') and request.POST.get('address') \
                and request.POST.get('labels'):
            c = Contents()
            if not request.user.id:
                c.user_id = request.POST.get('user_id')
                c.first_name = request.POST.get('first_name')
                c.last_name = request.POST.get('last_name')
            else:
                c.user_id = request.user.id
                c.first_name = request.user.first_name
                c.last_name = request.user.last_name
            c.title = request.POST.get('title')
            c.message = request.POST.get('message')
            c.address = request.POST.get('address')
            c.labels = request.POST.get('labels')
            c.origin = request.POST.get('origin')
            if request.POST.get('privacy'):
                if request.POST.get('privacy') == 'public':
                    c.private = False
                else:
                    c.private = True
            c.save()
            return render(request=request, template_name="main/home.html")
        else:
            messages.success(request, 'Please fill all areas!')
            return render(request=request, template_name="user_page/new_content.html")
    else:
        return render(request=request, template_name="user_page/new_content.html")


def my_profile(request):
    summary = ExtendedUser.objects.all().filter(user_id=request.user.id)
    if request.method == 'POST':
        if request.POST.get('summary'):
            if not summary:
                e = ExtendedUser()
                e.user_id = request.user.id
                e.summary = request.POST.get('summary')
                e.save()
                return render(request=request, template_name="user_page/my_profile.html",
                              context={"user": request.user, "summary": summary})
            else:
                ExtendedUser.objects.filter(user_id=request.user.id).update(summary=request.POST.get('summary'))
                return render(request=request, template_name="user_page/my_profile.html",
                              context={"user": request.user, "summary": summary})
    return render(request=request, template_name="user_page/my_profile.html", context={"user": request.user, "summary": summary})


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


def connections(request):
    User = get_user_model()
    all_users = User.objects.all()
    user_ids = all_users.values_list('id', flat=True)
    my_friends_ids = Friends.objects.all().filter(user_id=request.user.id).values_list('friend_ids', flat=True)
    friend_list = all_users.filter(id=0)
    is_friend = False
    if my_friends_ids:
        for f_id in my_friends_ids:
            friend_list = friend_list | all_users.filter(Q(id=f_id))
    if request.method == 'POST':
        if request.POST.get('search_user'):
            is_friend = True
            searched_user = request.POST.get('search_user')
            if searched_user != 'all':
                if my_friends_ids:
                    for f_id in my_friends_ids:
                        all_users = all_users.filter(Q(first_name__icontains=searched_user) | Q(last_name__icontains=searched_user)).exclude(Q(id=f_id))
            else:
                if my_friends_ids:
                    for f_id in my_friends_ids:
                        all_users = all_users.exclude(Q(id=f_id))
            return render(request=request, template_name="user_page/connections.html", context={"all_users": all_users, "is_friend": is_friend})
        elif request.POST.get('add'):
            for user_id in user_ids:
                if str(user_id) == request.POST.get('add') and str(request.user.id) != request.POST.get('add'):
                    add_friend_fail = True
                    f = Friends()
                    f.user_id = request.user.id
                    f.friend_ids = request.POST.get('add')
                    f.save()
                    contents = Contents.objects.all().order_by("-id")
                    return render(request=request, template_name="main/home.html", context={"contents": contents})
        elif request.POST.get('remove'):
            user_id = request.user.id
            f_id = request.POST.get('remove')
            member = Friends.objects.all().filter(Q(user_id=user_id) & Q(friend_ids=f_id))
            member.delete()
    return render(request=request, template_name="user_page/connections.html", context={"all_users": friend_list, "is_friend": is_friend})
