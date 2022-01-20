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

        if fname == "":
            messages.info(request, "Please enter your First name")
            return redirect("signup")
        elif lname == "":
            messages.info(request, "Please enter your Last name")
            return redirect("signup")
        elif email == "":
            messages.info(request, "Please enter your Email id")
            return redirect("signup") 
        elif uname == "":
            messages.info(request, "Please enter a Username")
            return redirect("signup") 
        elif pass1 == "" or pass2 == "":
            messages.info(request, "Please enter both the password fields.")
            return redirect("signup") 
        else:
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
                    return redirect("login")
                    # messages.info(request,"Registration completed")
                    # return redirect('signup')
            else:
                messages.info(request,"Passwords dont match. Please try again")
                return redirect("signup")

    else:
        return render(request, 'signup.html')

def login(request):
    if request.method == "POST":
        uname = request.POST['uname']
        pass1 = request.POST['pass1']
        
        if uname == "":
            messages.info(request, "Please enter the User Name")
            return redirect("login")
        elif pass1 == "":
            messages.info(request, "Please enter the Password")
            return redirect("login")
        else:

            user = auth.authenticate(username = uname, password = pass1)
            
            if user is not None:
                auth.login(request, user)
                return redirect("/")
            else:
                messages.info(request, "Invalid Credentials! Please try again.")
                return redirect("login")

    else:
        return render(request, "login.html")

def index(request):
    return render(request, "index.html")

def home(request):
    return render(request, "home.html")

def logout(request):
    auth.logout(request)
    return redirect("/")
