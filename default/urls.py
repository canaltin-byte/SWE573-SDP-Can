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
    path('', views.first_page, name='list'),
    path('test/', views.test, name='test'),
    path("register/", views.register_request, name="register"),
    path("login/", views.login_request, name="login"),
    path("logout/", views.logout_request, name="logout"),
    path("home/", views.home, name="test"),
    path("category/", views.category, name="category"),
    path("new_content/", views.new_content, name="new_content"),
    path("my_profile/", views.my_profile, name="my_profile")
]
