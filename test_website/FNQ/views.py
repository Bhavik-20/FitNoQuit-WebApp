from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth

# Create your views here.
def home(request):
    return render(request,'home.html')

def register(request):

    if request.method =='POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']

        if password1==password2:
            if User.objects.filter(username==username).exists():
                print('Username already exists :(')
            elif User.objects.filter(email==email).exists():
                print('Email already exists :(')

            else:
                user = User.objects.create_user(username=username, password=password1, email=email,first_name=first_name, last_name=last_name)
                user.save();
                print('user created')

        else:
            print('Password not matching..')
        return redirect('/')

    else:
        return render(request,'register.html')