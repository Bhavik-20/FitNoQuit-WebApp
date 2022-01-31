# from sys import last_traceback
from cProfile import Profile
from distutils.command.build_scripts import first_line_re
from pickle import FALSE, NONE
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.test import tag
import re

from matplotlib.style import use
from .models import Profile

email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
# phone_regex = r'^[0-9]{10}$'



def signup(request):
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        uname = request.POST['uname']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        
        if fname == "":
            # messages.info(request, "Please enter your First name")
            # return redirect("signup")
            context = { "fname" : "Please enter your First name", "lname" : "", "email": "", "uname": "", "pass": ""}
            return render(request, "signup.html", context)
        elif lname == "":
            # messages.info(request, "Please enter your Last name")
            # return redirect("signup")
            context = { "fname" : "", "lname" : "Please enter your Last name", "email": "", "uname": "", "pass": ""}
            return render(request, "signup.html", context)
        elif email == "" or re.fullmatch(email_regex, email) == None:
            # messages.info(request, "Please enter your Email id")
            # return redirect("signup") 
            context = { "fname" : "", "lname" : "", "email": "Please enter valid Email id", "uname": "", "pass": ""}
            return render(request, "signup.html", context)
        elif uname == "":
            # messages.info(request, "Please enter a Username")
            # return redirect("signup") 
            context = { "fname" : "", "lname" : "", "email": "", "uname": "Please enter a Username", "pass": ""}
            return render(request, "signup.html", context)
        elif pass1 == "" or pass2 == "":
            # messages.info(request, "Please enter both the password fields.")
            # return redirect("signup") 
            context = { "fname" : "", "lname" : "", "email": "", "uname": "", "pass": "Please enter both the password fields."} 
            return render(request, "signup.html", context)
        else:
            if pass1 == pass2:
                if User.objects.filter(email = email).exists():
                    # messages.info(request,"User with this Email already exists")
                    # return redirect("signup")
                    context = { "fname" : "", "lname" : "", "email": "User with this Email already exists", "uname": "", "pass": ""}
                    return render(request, "signup.html", context)
                elif User.objects.filter(username = uname).exists():
                    # messages.info(request,"User with this Username already exists")
                    # return redirect("signup")
                    context = { "fname" : "", "lname" : "", "email": "", "uname": "User with this Username already exists", "pass": ""}
                    return render(request, "signup.html", context)
                else:
                    user = User.objects.create_user(username = uname, email = email, first_name = fname, last_name = lname, password = pass1)
                    user.save();
                    user_profile = Profile.objects.create(uid = user, age=0, gender="----", height= 0.0, weight = 0.0, 
                                        bmi = 0.0, fitness_goal="----", curr_exercise=0, food_pref="----", health_issues="----", 
                                        fname= user.first_name, lname=user.last_name, email=user.email)
                    # user_profile.save();
                    print("Registration completed")
                    return redirect("login")
            else:
                # messages.info(request,"Passwords dont match. Please try again")
                # return redirect("signup")
                context = { "fname" : "", "lname" : "", "email": "", "uname": "", "pass": "Passwords dont match. Please try again"} 
                return render(request, "signup.html", context)

    else:
        return render(request, 'signup.html')

def login(request):
    if request.method == "POST":
        uname = request.POST['uname']
        pass1 = request.POST['pass1']
        if uname == "":
            # messages.info(request, "Please enter your User Name", extra_tags = "empty_uname")
            # return redirect("login") 
            context = { "uname" : "Please enter your User Name", "pass" : "", "final": "" }
            return render(request, "login.html", context)
        elif pass1 == "":
            # messages.info(request, "Please enter the Password", extra_tags = "empty_pass")
            # return redirect("login")
            context = { "uname" : "", "pass" : "Please enter your Password", "final": "" }
            return render(request, "login.html", context)
        else:
            user = auth.authenticate(username = uname, password = pass1)
            if user is not None:
                auth.login(request, user)
                return redirect("/")
            else:
                # messages.info(request, "Invalid Credentials! Please try again.", extra_tags = "invalid_creds")
                # return redirect("login")
                context = { "uname" : "", "pass" : "", "final": "Invalid Credentials! Please try again." }
                return render(request, "login.html", context)

    else:
        return render(request, "login.html")

def index(request):
    return render(request, "index.html")

def home(request):
    return render(request, "home.html")

def logout(request):
    auth.logout(request)
    return redirect("/")

def profile(request):
    if request.method == "POST":
        user_profile = Profile.objects.get(uid = request.user)
        height = request.POST['height']
        weight = request.POST['weight']
        age = request.POST['age']
        gender = request.POST['gender']
        fitness_goal = request.POST['fitness_goal']
        curr_exc = request.POST['curr_exc']
        food_pref = request.POST.get('food_pref',"----")
        health_issues = request.POST.get('health_issues',"----") #multiple input

        if height == "0.0":
            context = {"height":"Please enter valid Height in cms.","weight":"","age":"","gender":"",
            "fitness_goal":"", "curr_exc":"", "food_pref":"", "health_issues":"", "user_profile": user_profile}
            return render(request, "profile.html", context)
        elif weight == "0.00":
            context = {"height":"","weight":"Please enter valid Weight in kgs.","age":"","gender":"",
            "fitness_goal":"", "curr_exc":"", "food_pref":"", "health_issues":"", "user_profile": user_profile}
            return render(request, "profile.html", context)
        elif age == "0":
            context = {"height":"","weight":"","age":"Please enter valid Age in years.", "gender":"",
            "fitness_goal":"", "curr_exc":"", "food_pref":"", "health_issues":"", "user_profile": user_profile}
            return render(request, "profile.html", context)
        elif gender == "----":
            context = {"height":"","weight":"","age":"","gender":"Please select your Gender.",
            "fitness_goal":"", "curr_exc":"", "food_pref":"", "health_issues":"", "user_profile": user_profile}
            return render(request, "profile.html", context)
        elif fitness_goal == "----":
            context = {"height":"","weight":"","age":"","gender":"","fitness_goal":"Please select your fitness goal.", 
            "curr_exc":"", "food_pref":"", "health_issues":"", "user_profile": user_profile}
            return render(request, "profile.html", context)
        elif food_pref == "----":
            context = {"height":"","weight":"","age":"","gender":"", "fitness_goal":"", "curr_exc":"", 
            "food_pref":"Please select your food preference.", "health_issues":"", "user_profile": user_profile}
            return render(request, "profile.html", context)
        else:
            user_profile = Profile.objects.get(uid = request.user)
            user_profile.height = height
            user_profile.weight = weight
            user_profile.age = age
            user_profile.gender = gender
            user_profile.fitness_goal = fitness_goal
            user_profile.curr_exercise = curr_exc
            user_profile.food_pref = food_pref
            user_profile.health_issues = health_issues
            user_profile.save()
            context ={  "user_profile": user_profile }
            return render(request, "profile.html", context)
    else:
        user_profile = Profile.objects.get(uid = request.user)
        # fname = user_profile.fname
        # lname = user_profile.lname
        # email = user_profile.email

        return render(request, "profile.html",{'user_profile':user_profile} )