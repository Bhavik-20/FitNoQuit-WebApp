from django.shortcuts import render
from .models import Blogs
# Create your views here.

def blogs(request):
    get_blogs = Blogs.objects.get(blog_id=1)
    context={'sample': get_blogs.content}
    return render(request, "disp_blog.html",context)