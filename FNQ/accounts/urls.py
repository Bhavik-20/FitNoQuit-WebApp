from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name="home"),
    path("profile", views.profile, name="profile"),
    path("signup", views.signup, name="signup"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("diet", views.diet, name = "diet"),
    path("workout", views.workout, name = "workout"),
    path("wo_api",views.wo_api, name="wo_api"),
    path("view_workout",views.view_workout,name="view_workout")
]