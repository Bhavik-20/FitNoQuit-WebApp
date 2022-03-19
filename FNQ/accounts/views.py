# from sys import last_traceback
from cProfile import Profile
from distutils.command.build_scripts import first_line_re
from pickle import FALSE, NONE
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.test import tag
import re
import math
from .models import Profile, Diet

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
            context = { "fname" : "Please enter your First name", "lname" : "", "email": "", "uname": "", "pass": "",
            "fname1":fname,"lname1" : lname, "email1": email, "uname1": uname, "pass1": pass1}
            return render(request, "signup.html", context)
        elif lname == "":
            # messages.info(request, "Please enter your Last name")
            # return redirect("signup")
            context = { "fname" : "", "lname" : "Please enter your Last name", "email": "", "uname": "", "pass": "",
            "fname1":fname,"lname1" : lname, "email1": email, "uname1": uname, "pass1": pass1}
            return render(request, "signup.html", context)
        elif email == "" or re.fullmatch(email_regex, email) == None:
            # messages.info(request, "Please enter your Email id")
            # return redirect("signup") 
            context = { "fname" : "", "lname" : "", "email": "Please enter valid Email id", "uname": "", "pass": "",
            "fname1":fname,"lname1" : lname, "email1": email, "uname1": uname, "pass1": pass1}
            return render(request, "signup.html", context)
        elif uname == "":
            # messages.info(request, "Please enter a Username")
            # return redirect("signup") 
            context = { "fname" : "", "lname" : "", "email": "", "uname": "Please enter a Username", "pass": "",
            "fname1":fname,"lname1" : lname, "email1": email, "uname1": uname, "pass1": pass1}
            return render(request, "signup.html", context)
        elif pass1 == "" or pass2 == "":
            # messages.info(request, "Please enter both the password fields.")
            # return redirect("signup") 
            context = { "fname" : "", "lname" : "", "email": "", "uname": "", "pass": "Please enter both the password fields.",
            "fname1":fname,"lname1" : lname, "email1": email, "uname1": uname, "pass1": pass1} 
            return render(request, "signup.html", context)
        else:
            if pass1 == pass2:
                if User.objects.filter(email = email).exists():
                    # messages.info(request,"User with this Email already exists")
                    # return redirect("signup")
                    context = { "fname" : "", "lname" : "", "email": "User with this Email already exists", "uname": "", "pass": "",
                    "fname1":fname,"lname1" : lname, "email1": email, "uname1": uname, "pass1": pass1}
                    return render(request, "signup.html", context)
                elif User.objects.filter(username = uname).exists():
                    # messages.info(request,"User with this Username already exists")
                    # return redirect("signup")
                    context = { "fname" : "", "lname" : "", "email": "", "uname": "User with this Username already exists", "pass": "",
                    "fname1":fname,"lname1" : lname, "email1": email, "uname1": uname, "pass1": pass1}
                    return render(request, "signup.html", context)
                else:
                    user = User.objects.create_user(username = uname, email = email, first_name = fname, last_name = lname, password = pass1)
                    user.save();
                    user_profile = Profile.objects.create(uid = user, age=0, gender="----", height= 0.0, weight = 0.0, start_wt = 0.0, target_wt = 0.0,
                                        bmi = 0.0, fitness_goal="----", curr_exercise=0, food_pref="----", diabetes=False, kidney=False, 
                                        lactose=False, pcos=False, thyroid=False, fname= user.first_name, lname=user.last_name, email=user.email)
                    user_profile.save();
                    user_diet = Diet.objects.create(uid = user, diet_calories=0, plan_exists = False, is_vegan = False,
                                                    like_milk = True, like_seeds_nuts = True, like_sweets = True, 
                                                    like_fruits = True, like_salads = True, like_north = True, like_south = True)
                    user_diet.save();
                    print("Registration completed")
                    # return redirect("login")
                    context = {"dest": "login"}
                    return render(request, "loading.html", context)
            else:
                # messages.info(request,"Passwords dont match. Please try again")
                # return redirect("signup")
                context = { "fname" : "", "lname" : "", "email": "", "uname": "", "pass": "Passwords dont match. Please try again",
                "fname1":fname,"lname1" : lname, "email1": email, "uname1": uname, "pass1": pass1} 
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
            context = { "uname" : "Please enter your User Name", "pass" : "", "final": "", "uname1":uname, "pass1":pass1 }
            return render(request, "login.html", context)
        elif pass1 == "":
            # messages.info(request, "Please enter the Password", extra_tags = "empty_pass")
            # return redirect("login")
            context = { "uname" : "", "pass" : "Please enter your Password", "final": "", "uname1":uname, "pass1":pass1 }
            return render(request, "login.html", context)
        else:
            user = auth.authenticate(username = uname, password = pass1)
            if user is not None:
                auth.login(request, user)
                # return redirect("/")
                # user_profile = Profile.objects.get(uid = request.user)
                # context ={"user_profile": user_profile}
                context = {"dest": "dashboard"}
                return render(request, "loading.html",context)
                
            else:
                # messages.info(request, "Invalid Credentials! Please try again.", extra_tags = "invalid_creds")
                # return redirect("login")
                context = { "uname" : "", "pass" : "", "final": "Invalid Credentials! Please try again.", "uname1":uname, "pass1":pass1 }
                return render(request, "login.html", context)
    else:
        return render(request, "login.html")

def index(request):
    return render(request, "index.html")

def home(request):
    return render(request, "home.html")

def logout(request):
    auth.logout(request)
    context = {"dest": "home"}
    return render(request, "loading.html", context)
    
    # return redirect("/")

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
        diabetes = request.POST['diabetes']
        thyroid = request.POST['thyroid']
        pcos = request.POST['pcos']
        kidney = request.POST['kidney']
        lactose = request.POST['lactose']
        height_cm = float(height) 
        height_cm = height_cm / 100
        weight_kg = float(weight)
        bmi = weight_kg / (height_cm * height_cm)
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
        elif curr_exc == "----":
            context = {"height":"","weight":"","age":"","gender":"","fitness_goal":"", 
            "curr_exc":"Please select your current excercise level.", "food_pref":"", "health_issues":"", "user_profile": user_profile}
            return render(request, "profile.html", context)
        elif food_pref == "----":
            context = {"height":"","weight":"","age":"","gender":"", "fitness_goal":"", "curr_exc":"", 
            "food_pref":"Please select your food preference.", "health_issues":"", "user_profile": user_profile}
            return render(request, "profile.html", context)
        elif bmi < 18.5 and fitness_goal == "Weight Loss" or bmi < 18.5 and fitness_goal == "Maintain Health":
            context = {"height":"","weight":"","age":"","gender":"", "fitness_goal":"You are under weight! Please Select Weight Gain.", 
            "curr_exc":"", "food_pref":"", "health_issues":"", "user_profile": user_profile}
            return render(request, "profile.html", context)
        elif bmi > 25 and fitness_goal == "Weight Gain" or bmi > 25 and fitness_goal == "Maintain Health":
            context = {"height":"","weight":"","age":"","gender":"", "fitness_goal":"You are over weight! Please Select Weight Loss.", 
            "curr_exc":"", "food_pref":"", "health_issues":"", "user_profile": user_profile}
            return render(request, "profile.html", context)
        else:
            user_profile = Profile.objects.get(uid = request.user)
           
            if user_profile.start_wt == 0.0:
                user_profile.start_wt = weight
            if user_profile.fitness_goal != fitness_goal:
                user_profile.start_wt = weight
                if fitness_goal == "Weight Loss":
                    user_profile.target_wt = float(weight) - 1
                elif fitness_goal == "Weight Gain":
                    user_profile.target_wt = float(weight) + 1
            elif user_profile.fitness_goal == fitness_goal:
                if fitness_goal == "Weight Loss" and float(weight)<user_profile.target_wt:
                    user_profile.target_wt = weight
                elif fitness_goal == "Weight Gain" and float(weight)>user_profile.target_wt:
                    user_profile.target_wt = weight

            user_profile.height = height            
            user_profile.age = age
            user_profile.gender = gender            
            user_profile.curr_exercise = curr_exc
            user_profile.food_pref = food_pref
            user_profile.diabetes = diabetes
            user_profile.thyroid = thyroid
            user_profile.pcos = pcos
            user_profile.kidney = kidney
            user_profile.lactose = lactose
            user_profile.bmi = bmi
            user_profile.weight = weight
            user_profile.fitness_goal = fitness_goal
            
            user_profile.save()
            user_profile = Profile.objects.get(uid = request.user)
            context ={"user_profile": user_profile, "res": "Saved Successfully!"}
            return render(request, "profile.html", context)
    else:
        user_profile = Profile.objects.get(uid = request.user)
        return render(request, "profile.html",{'user_profile':user_profile} )

def dashboard(request):
    user_profile = Profile.objects.get(uid = request.user)
    user_diet = Diet.objects.get(uid = request.user)
    curr_bmi = user_profile.bmi
    
    curr_ht = user_profile.height
    curr_ht = float(curr_ht) 
    curr_ht = curr_ht / 100
    
    r1 = math.floor(24.99 * (curr_ht * curr_ht))
    r2 = math.ceil(18.5 * (curr_ht * curr_ht))
    wl = user_profile.start_wt - 1
    wg = user_profile.start_wt + 1
    if request.method == "GET":
        context = {'user_profile': user_profile, 'r1':r1, 'r2': r2, 'wl': wl, "wg": wg, 'user_diet':user_diet}
        return render(request, "dashboard.html",context)
    else:
        ent_target = request.POST['target_wt']
        user_profile.target_wt = ent_target
        
        if user_profile.fitness_goal == "Weight Loss" and user_profile.weight < float(user_profile.target_wt):
            user_profile.target_wt = user_profile.weight
        elif user_profile.fitness_goal == "Weight Gain" and user_profile.weight > float(user_profile.target_wt):
            user_profile.target_wt = user_profile.weight
        user_profile.save()
        user_profile = Profile.objects.get(uid = request.user)
        context = {'user_profile': user_profile, 'r1':r1, 'r2': r2, 'wl': wl, "wg": wg, 'user_diet':user_diet}
        return render(request, "dashboard.html",context)

def diet(request):
    if request.method == "POST":
        is_vegan = request.POST['vegan']
        like_milk = request.POST['milk']
        like_seeds_nuts = request.POST['seeds']
        like_sweets = request.POST['sweet']
        like_fruits = request.POST['fruits']
        like_salads =request.POST['salads']
        like_north = request.POST['n-cuisine']
        like_south = request.POST['s-cuisine']

        user_diet = Diet.objects.get(uid = request.user)
        user_diet.is_vegan = is_vegan
        user_diet.like_milk = like_milk
        user_diet.like_seeds_nuts = like_seeds_nuts
        user_diet.like_sweets = like_sweets
        user_diet.like_fruits = like_fruits
        user_diet.like_salads = like_salads
        user_diet.like_north = like_north
        user_diet.like_south = like_south
        user_diet.plan_exists = True
        user_diet.save()
        user_diet = Diet.objects.get(uid = request.user)
        context = {"dest": "dashboard", "user_diet":user_diet}
        return render(request, "loading.html",context)
        # return render(request, "dashboard.html")
    else:
        user_diet = Diet.objects.get(uid = request.user)
        context = {"user_diet":user_diet}
        return render(request, 'diet-qn.html', context)