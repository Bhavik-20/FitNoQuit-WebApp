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
    # if request.method == "POST":
        #categ = request.POST['category'] #will have to take this from previous page
    categ = "Weight Loss"
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