"""default URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('savsha/', include('savsha.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from default import settings
from savsha import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.first_page, name='first_page'),
    path("register/", views.register_request, name="register"),
    path("login/", views.login_request, name="login"),
    path("logout/", views.logout_request, name="logout"),
    path("home/", views.home, name="home"),
    path("new_content/", views.new_content, name="new_content"),
    path("my_profile/", views.my_profile, name="my_profile"),
    path("change_password/", views.PasswordChangeView.as_view(template_name="user_page/password_change.html"), name="change_password"),
    path("password_success/", views.password_success, name="password_success"),
    path("edit_profile/", views.UpdateUserView.as_view(), name="edit_user"),
    path("connections/", views.connections, name="connections"),
]
