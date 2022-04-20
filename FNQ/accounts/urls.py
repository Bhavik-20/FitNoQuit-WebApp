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
    path("view_workout",views.view_workout,name="view_workout"),
    path("bf_api",views.bf_api,name="view_bf"),
    path("ld_api",views.ld_api,name="view_ld"),
    path("snacks_api",views.snacks_api,name="view_snacks"),
    path('regenerate',views.regenerate, name= "regenerate"),
    path("view_diet",views.view_diet,name="view_diet")
]