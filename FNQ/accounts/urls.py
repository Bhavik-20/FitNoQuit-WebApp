from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name="home"),
    path("profile", views.profile, name="profile"),
    path("signup", views.signup, name="signup"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout")
]