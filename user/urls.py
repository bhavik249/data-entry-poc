from django.urls import path
from user.views import home, register_request, login_request, logout_request

app_name = "user" 

urlpatterns = [
    path("", home, name="home"),
    path("register/", register_request, name="register"),
    path("login/", login_request, name="login"),
    path("logout/", logout_request, name= "logout"),
]
