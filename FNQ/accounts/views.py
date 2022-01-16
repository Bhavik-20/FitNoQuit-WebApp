# from sys import last_traceback
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages


def signup(request):
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        uname = request.POST['uname']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if pass1 == pass2:
            if User.objects.filter(email = email).exists():
                messages.info(request,"User with this Email already exists")
                return redirect("signup")
            elif User.objects.filter(username = uname).exists():
                messages.info(request,"User with this Username already exists")
                return redirect("signup")
            else:
                user = User.objects.create_user(username = uname, email = email, first_name = fname, last_name = lname, password = pass1)
                user.save();
                print("Registration completed")
                # messages.info(request,"Registration completed")
                # return redirect('signup')
        else:
            messages.info(request,"Passwords dont match. Please try again")
            return redirect("signup")
        return redirect("/")

    else:
        return render(request, 'signup.html')

def index(request):
    return render(request, "index.html")