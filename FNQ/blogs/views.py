from django.shortcuts import render
from .models import Blogs
# Create your views here.

def view_blog(request):
    get_blogs = Blogs.objects.get(blog_id=3)
    context={'sample': get_blogs.content}
    return render(request, "disp_blog.html",context)

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
        for value in get_blogs.all():
            lst_title.append(value.title)
            lst_desc.append(value.content)
            lst_img.append(value.img)
        dicts = zip(lst_title, lst_desc, lst_img)
        context={'dicts': dicts, 'category': categ}
        return render(request, "blog_list.html",context)
