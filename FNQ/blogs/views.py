from unicodedata import category
from django.shortcuts import render
from .models import Blogs
# Create your views here.
from django.shortcuts import render, redirect

def view_blog(request):
    if request.method == "POST":
        blog_id = request.POST['blog_id']
        get_blogs = Blogs.objects.get(blog_id=blog_id)
        context={'blog_obj': get_blogs}
        return render(request, "blog_display.html",context)
    else:
        return redirect('/blogs/view_blog_categories')

def view_blog_categories(request):
    return render(request,"blog-categories.html")

def view_blog_list(request):
    if request.method == "POST":
        if 'weight-loss' in request.POST:
            categ = request.POST['weight-loss']
        elif 'weight-gain' in request.POST:
            categ = request.POST['weight-gain']
        elif 'healthy-lifestyle' in request.POST:
            categ = request.POST['healthy-lifestyle']
        elif 'nutrition' in request.POST:
            categ = request.POST['nutrition']
        elif 'recipes' in request.POST:
            categ = request.POST['recipes']
        elif 'workout' in request.POST:
            categ = request.POST['workout']
  
        get_blogs = Blogs.objects.filter(category=categ)
        lst_title = []
        lst_desc = []
        lst_img =[]
        lst_blogs=[]
        for value in get_blogs.all():
            lst_title.append(value.title)
            lst_desc.append(value.content)
            lst_img.append(value.img)
            lst_blogs.append(value.blog_id)
        dicts = zip(lst_title, lst_desc, lst_img, lst_blogs)
        context={'dicts': dicts, 'category': categ }
        return render(request, "blog_list.html",context)
    else:
        return redirect('/blogs/view_blog_categories')
