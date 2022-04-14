from django.urls import path
from . import views

urlpatterns = [
    path('view_blog',views.view_blog, name = "view_blog"),
    path('view_blog_categories',views.view_blog_categories, name="view_blog_categories"),
    path('view_blog_list',views.view_blog_list, name = "view_blog_list"),

]