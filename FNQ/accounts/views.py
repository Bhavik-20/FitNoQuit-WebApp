from asyncio.windows_events import NULL
from cProfile import Profile
from distutils.command.build_scripts import first_line_re
from pickle import FALSE, NONE
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.test import tag
import re
import math

from numpy import uint
from .models import Breakfast, Profile, Diet, Snacks, Workout, Lunch, Dinner
import json
import random
import validate_email_address
from validate_email_address import validate_email

email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
pass_regex = r"\b^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$\b"
def signup(request):
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        uname = request.POST['uname']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        is_valid_email = validate_email(email)
        print(is_valid_email)
        if fname == "":
            context = { "fname" : "Please enter your First name", "lname" : "", "email": "", "uname": "", "pass": "",
            "fname1":fname,"lname1" : lname, "email1": email, "uname1": uname, "pass1": pass1}
            return render(request, "signup.html", context)
        elif lname == "":
            context = { "fname" : "", "lname" : "Please enter your Last name", "email": "", "uname": "", "pass": "",
            "fname1":fname,"lname1" : lname, "email1": email, "uname1": uname, "pass1": pass1}
            return render(request, "signup.html", context)
        elif email == "" or re.fullmatch(email_regex, email) == None or is_valid_email == False:
            context = { "fname" : "", "lname" : "", "email": "Please enter valid Email id", "uname": "", "pass": "",
            "fname1":fname,"lname1" : lname, "email1": email, "uname1": uname, "pass1": pass1}
            return render(request, "signup.html", context)
        elif uname == "":
            context = { "fname" : "", "lname" : "", "email": "", "uname": "Please enter a Username", "pass": "",
            "fname1":fname,"lname1" : lname, "email1": email, "uname1": uname, "pass1": pass1}
            return render(request, "signup.html", context)
        elif pass1 == "" or pass2 == "": 
            context = { "fname" : "", "lname" : "", "email": "", "uname": "", "pass": "Please enter both the password fields.",
            "fname1":fname,"lname1" : lname, "email1": email, "uname1": uname, "pass1": pass1} 
            return render(request, "signup.html", context)
        else:
            if pass1 == pass2:
                if re.fullmatch(pass_regex, pass1) == None:
                    context = { "fname" : "", "lname" : "", "email": "", "uname": "", 
                                "pass": '''Password Should have at least one number.
                                            Should have at least one uppercase and one lowercase character.
                                            Should have at least one special symbol.
                                            Should be between 6 to 20 characters long''',
                    "fname1":fname,"lname1" : lname, "email1": email, "uname1": uname, "pass1": pass1} 
                    return render(request, "signup.html", context)
                elif User.objects.filter(email = email).exists():
                    context = { "fname" : "", "lname" : "", "email": "User with this Email already exists", "uname": "", "pass": "",
                    "fname1":fname,"lname1" : lname, "email1": email, "uname1": uname, "pass1": pass1}
                    return render(request, "signup.html", context)
                elif User.objects.filter(username = uname).exists():
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
                                                    like_fruits = True, like_salads = True, like_north = True, like_south = True, bf_protein = 0.0,
                                                    bf_carbs = 0.0, bf_fats = 0.0, ld_protein = 0.0, ld_carbs = 0.0, ld_fats = 0.0, 
                                                    snack_calories = 0.0)
                    user_diet.save();
                    user_bf = Breakfast.objects.create(uid = user)
                    user_bf.save();
                    user_l = Lunch.objects.create(uid = user)
                    user_l.save();
                    user_d = Dinner.objects.create(uid = user)
                    user_d.save();
                    user_s = Snacks.objects.create(uid = user)
                    user_s.save();
                    user_wo = Workout.objects.create(uid = user, wo_exists = False, wo_calories = 0, time = NULL, wo_type = NULL, 
                                                        sug_wo_cal = NULL, weight = 0.0, sug_wo_categories= NULL, sug_wo_name = NULL,
                                                         sug_wo_time = NULL)
                    user_wo.save();
                    context = {"dest": "login"}
                    return render(request, "loading.html", context)
            else:
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
            context = { "uname" : "Please enter your User Name", "pass" : "", "final": "", "uname1":uname, "pass1":pass1 }
            return render(request, "login.html", context)
        elif pass1 == "":
            context = { "uname" : "", "pass" : "Please enter your Password", "final": "", "uname1":uname, "pass1":pass1 }
            return render(request, "login.html", context)
        else:
            user = auth.authenticate(username = uname, password = pass1)
            if user is not None:
                auth.login(request, user)
                context = {"dest": "dashboard"}
                return render(request, "loading.html",context)
                
            else:
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
        elif pcos == "True" and gender == "male":
            context = {"height":"","weight":"","age":"","gender":"", "fitness_goal":"", 
            "curr_exc":"", "food_pref":"", "health_issues":"The health issue 'PCOS' doesn't apply to Males.", "user_profile": user_profile}
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


            bmr = 0
            if gender == 'male':
                bmr = 10 * float(weight) + 6.25 * float(height) - 5 * float(age) + 5
            elif gender == 'female':
                bmr = 10 * float(weight) + 6.25 * float(height) - 5 * float(age) - 161
            print("BMR =", bmr)

            workoutChoice = curr_exc

            tdee = 0
            if workoutChoice == "sedentary":
                tdee = bmr * 1.2
            elif workoutChoice == "lightly":
                tdee = bmr * 1.375
            elif workoutChoice == "moderately":
                tdee = bmr * 1.55
            elif workoutChoice == "very-active":
                tdee = bmr * 1.725
            elif workoutChoice == "extra-active":
                tdee = bmr * 1.9
            tdee = 0.9 * tdee
    
            targetChoice = fitness_goal

            totalCalories = tdee
            if targetChoice == "Weight Loss":
                totalCalories -= 500
            elif targetChoice == "Weight Gain":
                totalCalories += 200

            proteinCalories = 0
            carbsCalories = 0
            fatsCalories = 0

            if targetChoice == "Weight Loss":
                proteinCalories = 1.5 * float(weight) * 4
                carbsCalories = 0.5 * totalCalories
            else:
                if workoutChoice == "sedentary" or workoutChoice == "lightly":
                    proteinCalories = 1.25 * float(weight) * 4
                    carbsCalories = 0.55 * totalCalories
                else :
                    proteinCalories = 1.5 * float(weight) * 4
                    carbsCalories = 0.6 * totalCalories
            fatsCalories = totalCalories - (proteinCalories + carbsCalories)

            total = {'Protein': proteinCalories, 'Carbs': carbsCalories, 'Fats': fatsCalories}
            print(total)

            breakfast = {'Protein': 0.3 * proteinCalories, 'Carbs': 0.3 * carbsCalories, 'Fats': 0.3 * fatsCalories}
            print(breakfast)

            lunch = {'Protein': 0.35 * proteinCalories, 'Carbs': 0.35 * carbsCalories, 'Fats': 0.35 * fatsCalories}
            print(lunch)

            dinner = {'Protein': 0.35 * proteinCalories, 'Carbs': 0.35 * carbsCalories, 'Fats': 0.35 * fatsCalories}
            print(dinner)

            user_diet = Diet.objects.get(uid = request.user)
            if totalCalories >= 2500:
                snackCalories = 0.12 * totalCalories
            else:
                snackCalories = 0.10 * totalCalories
            user_diet.snack_calories = snackCalories
            user_diet.diet_calories = totalCalories
            user_diet.bf_carbs = breakfast['Carbs']
            user_diet.bf_fats = breakfast['Fats']
            user_diet.bf_protein = breakfast['Protein']
            user_diet.ld_carbs = lunch['Carbs']
            user_diet.ld_fats = lunch['Fats']
            user_diet.ld_protein = lunch['Protein']
            
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
            user_diet.save()

            user_profile = Profile.objects.get(uid = request.user)

            user_wo = Workout.objects.get(uid = request.user)
            user_wo.weight = weight
            user_wo.wo_calories = snackCalories * 0.67
            user_wo.save()

            context ={"user_profile": user_profile, "res": "Saved Successfully!"}
            return render(request, "profile.html", context)
    else:
        user_profile = Profile.objects.get(uid = request.user)
        return render(request, "profile.html",{'user_profile':user_profile} )

def dashboard(request):
    user_profile = Profile.objects.get(uid = request.user)
    user_diet = Diet.objects.get(uid = request.user)
    user_workout = Workout.objects.get(uid = request.user)
    curr_bmi = user_profile.bmi
    
    curr_ht = user_profile.height
    curr_ht = float(curr_ht) 
    curr_ht = curr_ht / 100
    
    r1 = math.floor(24.99 * (curr_ht * curr_ht))
    r2 = math.ceil(18.5 * (curr_ht * curr_ht))
    wl = user_profile.start_wt - 1
    wg = user_profile.start_wt + 1
    if request.method == "GET":
        context = {'user_profile': user_profile, 'r1':r1, 'r2': r2, 'wl': wl, "wg": wg, 'user_diet':user_diet, 'user_workout':user_workout}
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
        context = {'user_profile': user_profile, 'r1':r1, 'r2': r2, 'wl': wl, "wg": wg, 'user_diet':user_diet, 'user_workout':user_workout}
        return render(request, "dashboard.html",context)

def workout(request):
    if request.method=="POST":
        time = request.POST.getlist("time")
        wo_type = request.POST.getlist("type_exc")
        diet_plan = Diet.objects.get(uid = request.user).plan_exists
        msg=""
        if len(time)==0:
            msg = "Please select atleast one duration of time for workout."    
            context = {'msg':msg} 
            return render(request, "workout.html",context)
        elif len(wo_type) == 0:
            msg = "Please select atleast one type of movement you would like."
            context = {'msg':msg} 
            return render(request, "workout.html",context)
        elif diet_plan == False:
            msg = "Please start with the diet plan before generating a workout plan."
            context = {'msg':msg} 
            return render(request, "workout.html",context)
        user_wo = Workout.objects.get(uid = request.user)
        time = json.dumps(time)
        wo_type = json.dumps(wo_type)
        user_wo.time = time
        user_wo.wo_type = wo_type
        user_wo.save()
        context = {'dest': "wo_api",'msg': msg}
        return render(request, "loading.html",context)
    else:
        user_wo = Workout.objects.get(uid = request.user)
        context = {"user_wo": user_wo}
        return render(request, 'workout.html', context)

def view_workout(request):
    user_wo = Workout.objects.get(uid = request.user)
    if user_wo.wo_exists:
        wn = json.loads(user_wo.sug_wo_name)
        wot = json.loads(user_wo.sug_wo_time)
        wc = json.loads(user_wo.sug_wo_cal)
        wtype = json.loads(user_wo.sug_wo_categories)
        
        for i in range(len(wot)):
            wot[i] *= 60
        dicts = zip(wn,wtype, wot, wc)
        context = {'user_wo': user_wo, 'dicts': dicts}
        return render(request, "wo_disp.html",context)
    else:
        user_wo = Workout.objects.get(uid = request.user)
        context = {"user_wo": user_wo}
        return redirect('/workout',context)
        # return render(request, 'workout.html', context)

def wo_api(request):
    import pandas as pd
    import numpy as np
    import math

    df = pd.read_csv('accounts/wo_data.csv')

    wt1 = []
    wt2 = []
    wt3 = []
    wt4 = []
    for i in range(0, len(df['130 lb'])):
        wt1.append(130)
        wt2.append(155)
        wt3.append(180)
        wt4.append(205)
    df['weight1'] = wt1
    df['weight2'] = wt2
    df['weight3'] = wt3
    df['weight4'] = wt4

    c = []
    for i in range(0,len(df['130 lb'])):
        cf = 0
        c1 = df.loc[i][1] - (df['CPK'][i] * 60) 
        c2 = df.loc[i][2] - (df['CPK'][i] * 70) 
        c3 = df.loc[i][3] - (df['CPK'][i] * 82) 
        c4 = df.loc[i][4] - (df['CPK'][i] * 93)
        cf = (c1+c2+c3+c4)/4
        c.append(cf)
    c = sum(c) / len(c)

    user_wo = Workout.objects.get(uid = request.user)

    #################### Take from Database ##########################
    calories = user_wo.wo_calories

    time = json.loads(user_wo.time)
    time = [float(t) for t in time]
    
    wo_type = json.loads(user_wo.wo_type)   
    #################### Take from Database ##########################

    w = float(user_wo.weight)
    wn = []
    wot =[]
    wc = []
    dicts = {"Run_Walk": 0, "Sport_Recreation": 0, "Gym": 0}
    wtype = []

    count = len(df)
    vis = []
    while count > 0:
        i = random.randint(0,len(df)- 1)
        if i not in vis:
            vis.append(i)
            if df['Type'][i] in wo_type:
                cpk = df['CPK'][i]*w + c 
                for t in time:
                    if cpk * t <= calories+20 and cpk * t >= calories-20:
                        print("1: ", df['Type'][i],dicts[df['Type'][i]],dicts.get(df['Type'][i]))
                        if len(wo_type) == 1:
                            if dicts.get(df['Type'][i]) < 5:
                                dicts[df['Type'][i]] = dicts.get(df['Type'][i]) + 1
                                print("2: ", df['Type'][i], dicts[df['Type'][i]], dicts.get(df['Type'][i]))
                                wtype.append(df['Type'][i])
                                wn.append(df['Activity, Exercise or Sport (1 hour)'][i])
                                wot.append(t)
                                wc.append(math.ceil(cpk * t))
                        if dicts.get(df['Type'][i]) < 3:
                            dicts[df['Type'][i]] = dicts.get(df['Type'][i]) + 1
                            print("2: ", df['Type'][i], dicts[df['Type'][i]], dicts.get(df['Type'][i]))
                            wtype.append(df['Type'][i])
                            wn.append(df['Activity, Exercise or Sport (1 hour)'][i])
                            wot.append(t)
                            wc.append(math.ceil(cpk * t))
            count -= 1
                       
    user_wo = Workout.objects.get(uid = request.user)
    user_wo.sug_wo_name = json.dumps(wn)
    user_wo.sug_wo_time = json.dumps(wot)
    user_wo.sug_wo_cal = json.dumps(wc)
    user_wo.sug_wo_categories = json.dumps(wtype)
    user_wo.wo_exists = True
    user_wo.save()
    context = {'dest': "wo_disp"}
    return render(request, "loading.html",context)

def bf_api(request):
    import copy
    import pandas as pd
    import numpy as np
    import random

    allBreakfast = pd.read_csv('accounts/Breakfast-Datasets/Breakfast.csv')
    allBreakfast.dropna(inplace = True)
    allBreakfast.index = np.arange(1, len(allBreakfast) + 1)
    allBreakfast.index.name = 'Index'
    allBreakfastLength = allBreakfast.shape[0]

    allFruits = pd.read_csv('accounts/Breakfast-Datasets/Fruits.csv')
    allFruits.dropna(inplace = True)
    allFruits.index = np.arange(1, len(allFruits) + 1)
    allFruits.index.name = 'Index'
    allFruitsLength = allFruits.shape[0]

    allNuts = pd.read_csv('accounts/Breakfast-Datasets/Seeds and Nuts.csv')
    allNuts.dropna(inplace = True)
    allNuts.index = np.arange(1, len(allNuts) + 1)
    allNuts.index.name = 'Index'
    allNutsLength = allNuts.shape[0]
    
    allMilk = pd.read_csv('accounts/Breakfast-Datasets/Milk.csv')
    allMilk.dropna(inplace = True)
    allMilk.index = np.arange(1, len(allMilk) + 1)
    allMilk.index.name = 'Index'
    allMilkLength = allMilk.shape[0]

    allBreakfast['Breakfast Protein Calories'] = allBreakfast['Breakfast Protein'] * 4
    allBreakfast['Breakfast Carbs Calories'] = allBreakfast['Breakfast Carbs'] * 4
    allBreakfast['Breakfast Fats Calories'] = allBreakfast['Breakfast Fats'] * 9
    allBreakfast['Breakfast Total Calories'] = allBreakfast['Breakfast Protein'] * 4 + allBreakfast['Breakfast Carbs'] * 4 + allBreakfast['Breakfast Fats'] * 9

    allFruits['Fruits Protein Calories'] = allFruits['Fruits Protein'] * 4
    allFruits['Fruits Carbs Calories'] = allFruits['Fruits Carbs'] * 4
    allFruits['Fruits Fats Calories'] = allFruits['Fruits Fats'] * 9
    allFruits['Fruits Total Calories'] = allFruits['Fruits Protein'] * 4 + allFruits['Fruits Carbs'] * 4 + allFruits['Fruits Fats'] * 9

    allNuts['Nuts Protein Calories'] = allNuts['Nuts Protein'] * 4
    allNuts['Nuts Carbs Calories'] = allNuts['Nuts Carbs'] * 4
    allNuts['Nuts Fats Calories'] = allNuts['Nuts Fats'] * 9
    allNuts['Nuts Total Calories'] = allNuts['Nuts Protein'] * 4 + allNuts['Nuts Carbs'] * 4 + allNuts['Nuts Fats'] * 9

    allMilk['Milk Protein Calories'] = allMilk['Milk Protein'] * 4
    allMilk['Milk Carbs Calories'] = allMilk['Milk Carbs'] * 4
    allMilk['Milk Fats Calories'] = allMilk['Milk Fats'] * 9
    allMilk['Milk Total Calories'] = allMilk['Milk Protein'] * 4 + allMilk['Milk Carbs'] * 4 + allMilk['Milk Fats'] * 9

    allBreakfast.drop(['Breakfast Protein', 'Breakfast Carbs', 'Breakfast Fats'], axis = 1, inplace = True)
    allFruits.drop(['Fruits Protein', 'Fruits Carbs', 'Fruits Fats'], axis = 1, inplace = True)
    allNuts.drop(['Nuts Protein', 'Nuts Carbs', 'Nuts Fats'], axis = 1, inplace = True)
    allMilk.drop(['Milk Protein', 'Milk Carbs', 'Milk Fats'], axis = 1, inplace = True)

    user_diet = Diet.objects.get(uid = request.user)
    user_profile = Profile.objects.get(uid = request.user)

    if user_profile.food_pref == "veg":
        isVeg =  "Y"
    else:
        isVeg =  "N"
    
    if user_profile.diabetes:
        diabetes = "Y"
    else:
        diabetes = "N"

    if user_profile.thyroid:
        thyroid = "Y"
    else:
        thyroid = "N"

    if user_profile.pcos:
        pcos = "Y"
    else:
        pcos = "N"

    if user_profile.kidney:
        kidney = "Y"
    else:
        kidney = "N"

    if user_profile.lactose:
        lactoseIntolerant = "Y"
    else:
        lactoseIntolerant = "N"
    
    if user_diet.is_vegan:
        vegan = "Y"
    else:
        vegan = "N"
    
    if user_diet.like_milk:
        likeMilk = "Y"
    else:
        likeMilk = "N"
    
    if user_diet.like_fruits:
        likeFruits = "Y"
    else:
        likeFruits = "N"

    if user_diet.like_seeds_nuts:
        likeNuts = "Y"
    else:
        likeNuts = "N"
        

    # print("NUTSSSSSSS 1: " + likeNuts)
    cuisine = ["General"]
    if user_diet.like_north:
        cuisine.append("North Indian")
    
    if user_diet.like_south:
        cuisine.append("South Indian")


    breakfast = allBreakfast
    fruits = allFruits
    nuts = allNuts
    milk = allMilk

    breakfast = breakfast[breakfast['Cuisine (North Indian/ South Indian/ General)'].isin(cuisine)]

    if isVeg == 'Y':
        breakfast = breakfast[breakfast['Type (Veg/ Non Veg)'] == 'Veg']
        fruits = fruits[fruits['Type (Veg/ Non Veg)'] == 'Veg']
        nuts = nuts[nuts['Type (Veg/ Non Veg)'] == 'Veg']

    if diabetes == 'Y':
        breakfast = breakfast[breakfast['Diabetes'] == 'Y']
        fruits = fruits[fruits['Diabetes'] == 'Y']
        nuts = nuts[nuts['Diabetes'] == 'Y']
        milk = milk[milk['Diabetes'] == 'Y']

    if thyroid == 'Y':
        breakfast = breakfast[breakfast['Thyroid'] == 'Y']
        fruits = fruits[fruits['Thyroid'] == 'Y']
        nuts = nuts[nuts['Thyroid'] == 'Y']
        milk = milk[milk['Thyroid'] == 'Y']

    if pcos == 'Y':
        breakfast = breakfast[breakfast['PCOS'] == 'Y']
        fruits = fruits[fruits['PCOS'] == 'Y']
        nuts = nuts[nuts['PCOS'] == 'Y']
        milk = milk[milk['PCOS'] == 'Y']

    if kidney == 'Y':
        breakfast = breakfast[breakfast['Kidney'] == 'Y']
        fruits = fruits[fruits['Kidney'] == 'Y']
        nuts = nuts[nuts['Kidney'] == 'Y']
        milk = milk[milk['Kidney'] == 'Y']

    if lactoseIntolerant == 'Y':
        breakfast = breakfast[breakfast['Lactose Intolerant'] == 'Y']
        fruits = fruits[fruits['Lactose Intolerant'] == 'Y']
        nuts = nuts[nuts['Lactose Intolerant'] == 'Y']
        milk = milk[milk['Lactose Intolerant'] == 'Y']

    if vegan == 'Y':
        breakfast = breakfast[breakfast['Vegan'] == 'Y']
        fruits = fruits[fruits['Vegan'] == 'Y']
        nuts = nuts[nuts['Vegan'] == 'Y']
        milk = milk[milk['Vegan'] == 'Y']

    breakfast.drop(['Diabetes', 'Thyroid', 'PCOS', 'Kidney', 'Lactose Intolerant', 'Vegan', 'Type (Veg/ Non Veg)',
                    'Cuisine (North Indian/ South Indian/ General)'], axis=1, inplace=True)
    fruits.drop(['Diabetes', 'Thyroid', 'PCOS', 'Kidney', 'Lactose Intolerant', 'Vegan', 'Type (Veg/ Non Veg)'], axis=1,
                inplace=True)
    nuts.drop(['Diabetes', 'Thyroid', 'PCOS', 'Kidney', 'Lactose Intolerant', 'Vegan', 'Type (Veg/ Non Veg)'], axis=1,
            inplace=True)
    milk.drop(['Diabetes', 'Thyroid', 'PCOS', 'Kidney', 'Lactose Intolerant', 'Vegan'], axis=1, inplace=True)

    
    breakfastLength = breakfast.shape[0]
    fruitsLength = fruits.shape[0]
    milkLength = milk.shape[0]
    nutsLength = nuts.shape[0]
    user_diet = Diet.objects.get(uid = request.user)
    print("Nuts Length:", nutsLength)
    if fruitsLength == 0:
        likeFruits = 'N'
        user_diet.like_fruits = False
    if milkLength == 0:
        likeMilk = 'N'
        user_diet.like_milk = False
    if nutsLength == 0:
        likeNuts = 'N'
        user_diet.like_seeds_nuts = False
    user_diet.save()
    breakfastMeal = breakfast
    if likeFruits == 'Y':
        breakfastMeal = pd.merge(breakfastMeal, fruits, how='cross')

    if likeMilk == 'Y':
        breakfastMeal = pd.merge(breakfastMeal, milk, how='cross')

    if likeNuts == 'Y':
        breakfastMeal = pd.merge(breakfastMeal, nuts, how='cross')

    breakfastMeal['Protein Calories'] = breakfastMeal['Breakfast Protein Calories']
    breakfastMeal['Carbs Calories'] = breakfastMeal['Breakfast Carbs Calories']
    breakfastMeal['Fats Calories'] = breakfastMeal['Breakfast Fats Calories']
    breakfastMeal['Total Calories'] = breakfastMeal['Breakfast Total Calories']
    if likeFruits == 'Y':
        breakfastMeal['Protein Calories'] += breakfastMeal['Fruits Protein Calories']
        breakfastMeal['Carbs Calories'] += breakfastMeal['Fruits Carbs Calories']
        breakfastMeal['Fats Calories'] += breakfastMeal['Fruits Fats Calories']
        breakfastMeal['Total Calories'] += breakfastMeal['Fruits Total Calories']

    if likeMilk == 'Y':
        breakfastMeal['Protein Calories'] += breakfastMeal['Milk Protein Calories']
        breakfastMeal['Carbs Calories'] += breakfastMeal['Milk Carbs Calories']
        breakfastMeal['Fats Calories'] += breakfastMeal['Milk Fats Calories']
        breakfastMeal['Total Calories'] += breakfastMeal['Milk Total Calories']

    if likeNuts == 'Y':
        breakfastMeal['Protein Calories'] += breakfastMeal['Nuts Protein Calories']
        breakfastMeal['Carbs Calories'] += breakfastMeal['Nuts Carbs Calories']
        breakfastMeal['Fats Calories'] += breakfastMeal['Nuts Fats Calories']
        breakfastMeal['Total Calories'] += breakfastMeal['Nuts Total Calories']

    breakfastMeal.index = np.arange(1, len(breakfastMeal) + 1)
    breakfastMeal.index.name = 'Index'
    breakfastMealLength = breakfastMeal.shape[0]


    targetCalories = {'Protein': 0, 'Carbs': 0, 'Fats': 0, 'Total': 0}
    targetCalories['Protein'] = float(user_diet.bf_protein)
    targetCalories['Carbs'] = float(user_diet.bf_carbs)
    targetCalories['Fats'] = float(user_diet.bf_fats)
    targetCalories['Total'] =  targetCalories['Protein'] +  targetCalories['Carbs'] +  targetCalories['Fats']

    breakfastMeal['Total Protein Error'] = abs(breakfastMeal['Protein Calories'] - targetCalories['Protein'])
    breakfastMeal['Total Carbs Error'] = abs(breakfastMeal['Carbs Calories'] - targetCalories['Carbs'])
    breakfastMeal['Total Fats Error'] = abs(breakfastMeal['Fats Calories'] - targetCalories['Fats'])
    breakfastMeal['Total Error'] = breakfastMeal['Total Protein Error'] + breakfastMeal['Total Carbs Error'] + breakfastMeal['Total Fats Error']

    selected = {}
    prevLen = -1
    margin = 100
    while len(selected) <= 50 and len(selected) != prevLen and margin <= 200:
        selected = breakfastMeal[breakfastMeal['Total Error'] <= margin]
        margin += 5
    selected.index = np.arange(1, len(selected) + 1)
    selected.index.name = 'Index'

    selectedLen = len(selected)
    for i in range(1, selectedLen + 1):
        print(i)
        prev = 0
        curr = selected.loc[i]
        counter = 0
        breakfastRate = 0.05
        milkRate = 0.03
        fruitsRate = 0.03
        nutsRate = 0.02
        while curr.equals(other=prev) == False and counter < 100:
            prev = copy.deepcopy(curr)
            if curr['Protein Calories'] < 0.95 * targetCalories['Protein']:
                if curr['Breakfast Quantity'] < selected.loc[i, 'Breakfast Quantity'] * 1.8:
                    curr['Breakfast Quantity'] += breakfastRate * selected.loc[i, 'Breakfast Quantity']
                    curr['Breakfast Protein Calories'] += breakfastRate * selected.loc[i, 'Breakfast Protein Calories']
                    curr['Breakfast Carbs Calories'] += breakfastRate * selected.loc[i, 'Breakfast Carbs Calories']
                    curr['Breakfast Fats Calories'] += breakfastRate * selected.loc[i, 'Breakfast Fats Calories']
                if likeMilk == 'Y':
                    if curr['Milk Quantity'] < selected.loc[i, 'Milk Quantity'] * 1.4:
                        curr['Milk Quantity'] += milkRate * selected.loc[i, 'Milk Quantity']
                        curr['Milk Protein Calories'] += milkRate * selected.loc[i, 'Milk Protein Calories']
                        curr['Milk Carbs Calories'] += milkRate * selected.loc[i, 'Milk Carbs Calories']
                        curr['Milk Fats Calories'] += milkRate * selected.loc[i, 'Milk Fats Calories']
            if curr['Protein Calories'] > 1.05 * targetCalories['Protein']:
                if curr['Breakfast Quantity'] > selected.loc[i, 'Breakfast Quantity'] * 0.8:
                    curr['Breakfast Quantity'] -= breakfastRate * selected.loc[i, 'Breakfast Quantity']
                    curr['Breakfast Protein Calories'] -= breakfastRate * selected.loc[i, 'Breakfast Protein Calories']
                    curr['Breakfast Carbs Calories'] -= breakfastRate * selected.loc[i, 'Breakfast Carbs Calories']
                    curr['Breakfast Fats Calories'] -= breakfastRate * selected.loc[i, 'Breakfast Fats Calories']
                if likeMilk == 'Y':
                    if curr['Milk Quantity'] > selected.loc[i, 'Milk Quantity'] * 0.4:
                        curr['Milk Quantity'] -= milkRate * selected.loc[i, 'Milk Quantity']
                        curr['Milk Protein Calories'] -= milkRate * selected.loc[i, 'Milk Protein Calories']
                        curr['Milk Carbs Calories'] -= milkRate * selected.loc[i, 'Milk Carbs Calories']
                        curr['Milk Fats Calories'] -= milkRate * selected.loc[i, 'Milk Fats Calories']

            if curr['Carbs Calories'] < 0.95 * targetCalories['Carbs']:
                if curr['Breakfast Quantity'] < selected.loc[i, 'Breakfast Quantity'] * 1.8:
                    curr['Breakfast Quantity'] += breakfastRate * selected.loc[i, 'Breakfast Quantity']
                    curr['Breakfast Protein Calories'] += breakfastRate * selected.loc[i, 'Breakfast Protein Calories']
                    curr['Breakfast Carbs Calories'] += breakfastRate * selected.loc[i, 'Breakfast Carbs Calories']
                    curr['Breakfast Fats Calories'] += breakfastRate * selected.loc[i, 'Breakfast Fats Calories']
                if likeFruits == 'Y':
                    if curr['Fruits Quantity'] < selected.loc[i, 'Fruits Quantity'] * 1.8:
                        curr['Fruits Quantity'] += fruitsRate * selected.loc[i, 'Fruits Quantity']
                        curr['Fruits Protein Calories'] += fruitsRate * selected.loc[i, 'Fruits Protein Calories']
                        curr['Fruits Carbs Calories'] += fruitsRate * selected.loc[i, 'Fruits Carbs Calories']
                        curr['Fruits Fats Calories'] += fruitsRate * selected.loc[i, 'Fruits Fats Calories']
                if likeMilk == 'Y':
                    if curr['Milk Quantity'] < selected.loc[i, 'Milk Quantity'] * 1.4:
                        curr['Milk Quantity'] += milkRate * selected.loc[i, 'Milk Quantity']
                        curr['Milk Protein Calories'] += milkRate * selected.loc[i, 'Milk Protein Calories']
                        curr['Milk Carbs Calories'] += milkRate * selected.loc[i, 'Milk Carbs Calories']
                        curr['Milk Fats Calories'] += milkRate * selected.loc[i, 'Milk Fats Calories']
            if curr['Carbs Calories'] > 1.05 * targetCalories['Carbs']:
                if curr['Breakfast Quantity'] > selected.loc[i, 'Breakfast Quantity'] * 0.8:
                    curr['Breakfast Quantity'] -= breakfastRate * selected.loc[i, 'Breakfast Quantity']
                    curr['Breakfast Protein Calories'] -= breakfastRate * selected.loc[i, 'Breakfast Protein Calories']
                    curr['Breakfast Carbs Calories'] -= breakfastRate * selected.loc[i, 'Breakfast Carbs Calories']
                    curr['Breakfast Fats Calories'] -= breakfastRate * selected.loc[i, 'Breakfast Fats Calories']
                if likeFruits == 'Y':
                    if curr['Fruits Quantity'] > selected.loc[i, 'Fruits Quantity'] * 0.5:
                        curr['Fruits Quantity'] -= fruitsRate * selected.loc[i, 'Fruits Quantity']
                        curr['Fruits Protein Calories'] -= fruitsRate * selected.loc[i, 'Fruits Protein Calories']
                        curr['Fruits Carbs Calories'] -= fruitsRate * selected.loc[i, 'Fruits Carbs Calories']
                        curr['Fruits Fats Calories'] -= fruitsRate * selected.loc[i, 'Fruits Fats Calories']
                if likeMilk == 'Y':
                    if curr['Milk Quantity'] > selected.loc[i, 'Milk Quantity'] * 0.4:
                        curr['Milk Quantity'] -= milkRate * selected.loc[i, 'Milk Quantity']
                        curr['Milk Protein Calories'] -= milkRate * selected.loc[i, 'Milk Protein Calories']
                        curr['Milk Carbs Calories'] -= milkRate * selected.loc[i, 'Milk Carbs Calories']
                        curr['Milk Fats Calories'] -= milkRate * selected.loc[i, 'Milk Fats Calories']

            if curr['Fats Calories'] < 0.95 * targetCalories['Fats']:
                if curr['Breakfast Quantity'] < selected.loc[i, 'Breakfast Quantity'] * 1.8:
                    curr['Breakfast Quantity'] += breakfastRate * selected.loc[i, 'Breakfast Quantity']
                    curr['Breakfast Protein Calories'] += breakfastRate * selected.loc[i, 'Breakfast Protein Calories']
                    curr['Breakfast Carbs Calories'] += breakfastRate * selected.loc[i, 'Breakfast Carbs Calories']
                    curr['Breakfast Fats Calories'] += breakfastRate * selected.loc[i, 'Breakfast Fats Calories']
                if likeNuts == 'Y':
                    if curr['Nuts Quantity'] < selected.loc[i, 'Nuts Quantity'] * 1.4:
                        curr['Nuts Quantity'] += nutsRate * selected.loc[i, 'Nuts Quantity']
                        curr['Nuts Protein Calories'] += nutsRate * selected.loc[i, 'Nuts Protein Calories']
                        curr['Nuts Carbs Calories'] += nutsRate * selected.loc[i, 'Nuts Carbs Calories']
                        curr['Nuts Fats Calories'] += nutsRate * selected.loc[i, 'Nuts Fats Calories']
                if likeMilk == 'Y':
                    if curr['Milk Quantity'] < selected.loc[i, 'Milk Quantity'] * 1.4:
                        curr['Milk Quantity'] += milkRate * selected.loc[i, 'Milk Quantity']
                        curr['Milk Protein Calories'] += milkRate * selected.loc[i, 'Milk Protein Calories']
                        curr['Milk Carbs Calories'] += milkRate * selected.loc[i, 'Milk Carbs Calories']
                        curr['Milk Fats Calories'] += milkRate * selected.loc[i, 'Milk Fats Calories']
            if curr['Fats Calories'] > 1.05 * targetCalories['Fats']:
                if curr['Breakfast Quantity'] > selected.loc[i, 'Breakfast Quantity'] * 0.8:
                    curr['Breakfast Quantity'] -= breakfastRate * selected.loc[i, 'Breakfast Quantity']
                    curr['Breakfast Protein Calories'] -= breakfastRate * selected.loc[i, 'Breakfast Protein Calories']
                    curr['Breakfast Carbs Calories'] -= breakfastRate * selected.loc[i, 'Breakfast Carbs Calories']
                    curr['Breakfast Fats Calories'] -= breakfastRate * selected.loc[i, 'Breakfast Fats Calories']
                if likeNuts == 'Y':
                    if curr['Nuts Quantity'] > selected.loc[i, 'Nuts Quantity'] * 0.5:
                        curr['Nuts Quantity'] -= nutsRate * selected.loc[i, 'Nuts Quantity']
                        curr['Nuts Protein Calories'] -= nutsRate * selected.loc[i, 'Nuts Protein Calories']
                        curr['Nuts Carbs Calories'] -= nutsRate * selected.loc[i, 'Nuts Carbs Calories']
                        curr['Nuts Fats Calories'] -= nutsRate * selected.loc[i, 'Nuts Fats Calories']
                if likeMilk == 'Y':
                    if curr['Milk Quantity'] > selected.loc[i, 'Milk Quantity'] * 0.4:
                        curr['Milk Quantity'] -= milkRate * selected.loc[i, 'Milk Quantity']
                        curr['Milk Protein Calories'] -= milkRate * selected.loc[i, 'Milk Protein Calories']
                        curr['Milk Carbs Calories'] -= milkRate * selected.loc[i, 'Milk Carbs Calories']
                        curr['Milk Fats Calories'] -= milkRate * selected.loc[i, 'Milk Fats Calories']

            curr['Breakfast Total Calories'] = curr['Breakfast Protein Calories'] + curr['Breakfast Carbs Calories'] + curr[
                'Breakfast Fats Calories']
            curr['Protein Calories'] = curr['Breakfast Protein Calories']
            curr['Carbs Calories'] = curr['Breakfast Carbs Calories']
            curr['Fats Calories'] = curr['Breakfast Fats Calories']
            if likeFruits == 'Y':
                curr['Fruits Total Calories'] = curr['Fruits Protein Calories'] + curr['Fruits Carbs Calories'] + curr[
                    'Fruits Fats Calories']
                curr['Protein Calories'] += curr['Fruits Protein Calories']
                curr['Carbs Calories'] += curr['Fruits Carbs Calories']
                curr['Fats Calories'] += curr['Fruits Fats Calories']
            if likeMilk == 'Y':
                curr['Milk Total Calories'] = curr['Milk Protein Calories'] + curr['Milk Carbs Calories'] + curr[
                    'Milk Fats Calories']
                curr['Protein Calories'] += curr['Milk Protein Calories']
                curr['Carbs Calories'] += curr['Milk Carbs Calories']
                curr['Fats Calories'] += curr['Milk Fats Calories']
            if likeNuts == 'Y':
                curr['Nuts Total Calories'] = curr['Nuts Protein Calories'] + curr['Nuts Carbs Calories'] + curr[
                    'Nuts Fats Calories']
                curr['Protein Calories'] += curr['Nuts Protein Calories']
                curr['Carbs Calories'] += curr['Nuts Carbs Calories']
                curr['Fats Calories'] += curr['Nuts Fats Calories']

            curr['Total Calories'] = curr['Protein Calories'] + curr['Carbs Calories'] + curr['Fats Calories']
            curr['Total Protein Error'] = abs(curr['Protein Calories'] - targetCalories['Protein'])
            curr['Total Carbs Error'] = abs(curr['Carbs Calories'] - targetCalories['Carbs'])
            curr['Total Fats Error'] = abs(curr['Fats Calories'] - targetCalories['Fats'])
            curr['Total Error'] = curr['Total Protein Error'] + curr['Total Carbs Error'] + curr['Total Fats Error']

            counter += 1
        selected.loc[i] = curr

    choices = 1
    df1 = {}
    df2 = {}
    prevLen = -1
    proteinMargin = 20
    carbsMargin = 20
    fatsMargin = 20

    while len(df1) <= 5 and prevLen != len(df1) and carbsMargin <= 40 and fatsMargin <= 40:
        df1 = selected.sort_values('Total Error')[selected['Total Carbs Error'] <= carbsMargin][selected['Total Fats Error'] <= fatsMargin][selected['Total Protein Error'] <= proteinMargin]
        proteinMargin += 1
        carbsMargin += 1
        fatsMargin += 1

    prevLen = -1
    proteinMargin = 41
    carbsMargin = 20
    fatsMargin = 20
    while len(df2) <= 5 and prevLen != len(df2) and carbsMargin <= 40 and fatsMargin <= 40:
        df2 = selected.sort_values('Total Error')[selected['Total Carbs Error'] <= carbsMargin][selected['Total Fats Error'] <= fatsMargin][selected['Total Protein Error'] >= proteinMargin][selected['Total Protein Error'] <= 100]
        carbsMargin += 1
        fatsMargin += 1
        proteinMargin += 1

    choices = pd.concat([df1, df2])

    while len(choices['Breakfast Name'].unique()) <= 10:
        choices = choices.append(breakfastMeal.iloc[random.randint(0, len(breakfastMeal) - 1)], ignore_index = True)

    choices.index = np.arange(1, len(choices) + 1)
    choices.index.name = 'Index'
    choicesLength = choices.shape[0]

    choices['Protein Powder'] = 0
    for i in range (1, choicesLength + 1):
        if choices.loc[i, "Total Protein Error"] >= 41:
            choices.loc[i, "Protein Powder"] = choices.loc[i, "Total Protein Error"] / 4
        else:
            choices.loc[i, "Protein Powder"] = 0

    finalChoices = []
    al = []
    bl = []
    cl = []
    dl = []
    el =[]
    # print("NUTSSSSSSSSSSSSS:" + likeNuts)
    for j in range(0, 3):
        i = random.randint(1, len(choices))
        s = "Main: " + choices.loc[i, "Breakfast Name"] + ", Quantity: " + str(float("{:.2f}".format(choices.loc[i, "Breakfast Quantity"])))
        aa = choices.loc[i, "Breakfast Name"] + " (" + str(float("{:.2f}".format(choices.loc[i, "Breakfast Quantity"]))) + " g)"
        al.append(aa)
        if likeMilk == "Y":
            s += "; " + "Milk: " + choices.loc[i, "Milk Name"] + ", Quantity: " + str(float("{:.2f}".format(choices.loc[i, "Milk Quantity"])))
            bb = choices.loc[i, "Milk Name"] + " (" + str(float("{:.2f}".format(choices.loc[i, "Milk Quantity"]))) + " g)"
            bl.append(bb)
        else:
            bl.append("None")
        if likeFruits == "Y":
            s += "; " + "Fruit: " + choices.loc[i, "Fruits Name"] + ", Quantity: " + str(float("{:.2f}".format(choices.loc[i, "Fruits Quantity"])))
            cc = choices.loc[i, "Fruits Name"] + " (" + str(float("{:.2f}".format(choices.loc[i, "Fruits Quantity"]))) + " g)"
            cl.append(cc)
        else:
            cl.append("None")
        if likeNuts == "Y":
            s += "; " + "Nut: " + choices.loc[i, "Nuts Name"] + ", Quantity: " + str(float("{:.2f}".format(choices.loc[i, "Nuts Quantity"])))
            dd = choices.loc[i, "Nuts Name"] + " (" + str(float("{:.2f}".format(choices.loc[i, "Nuts Quantity"]))) + " g)"
            dl.append(dd)
        else:
            dl.append("None")
        s += "; " + "Protein Powder: " + str(float("{:.2f}".format(choices.loc[i, "Protein Powder"])))
        ee = str(float("{:.2f}".format(choices.loc[i, "Protein Powder"]))) + " g"
        el.append(ee)
        finalChoices.append(s)
    print(finalChoices)
    user_bf = Breakfast.objects.get(uid = request.user)
    user_bf.bf_main_1 = al[0]
    user_bf.bf_main_2 = al[1]
    user_bf.bf_main_3 = al[2]
    user_bf.bf_milk_1 = bl[0]
    user_bf.bf_milk_2 = bl[1]
    user_bf.bf_milk_3 = bl[2]
    user_bf.bf_fruits_1 = cl[0]
    user_bf.bf_fruits_2 = cl[1]
    user_bf.bf_fruits_3 = cl[2]
    user_bf.bf_nuts_1 = dl[0]
    user_bf.bf_nuts_2 = dl[1]
    user_bf.bf_nuts_3 = dl[2]
    user_bf.bf_pp_1 = el[0]
    user_bf.bf_pp_2 = el[1]
    user_bf.bf_pp_3 = el[2]
    choices = choices.to_json()
    user_bf.choices = json.dumps(choices)
    user_bf.save()
    context = {"dest":"ld_api"}
    return render(request,"loading_diet.html", context)

def ld_api(request):
    import copy
    import pandas as pd
    import numpy as np
    import random


    allMainHP = pd.read_csv("accounts/LnD-Datasets/Lunch and Dinner - High Protein.csv")
    allMainHP.dropna(inplace = True)
    allMainHP.index = np.arange(1, len(allMainHP) + 1)
    allMainHP.index.name = 'Index'
    allMainHPLength = allMainHP.shape[0]

    allMainLP = pd.read_csv('accounts/LnD-Datasets/Lunch and Dinner - Low Protein.csv')
    allMainLP.dropna(inplace = True)
    allMainLP.index = np.arange(1, len(allMainLP) + 1)
    allMainLP.index.name = 'Index'
    allMainLPLength = allMainLP.shape[0]

    allSides = pd.read_csv('accounts/LnD-Datasets/Roti and Rice.csv')
    allSides.dropna(inplace = True)
    allSides.index = np.arange(1, len(allSides) + 1)
    allSides.index.name = 'Index'
    allSidesLength = allSides.shape[0]

    allSalads = pd.read_csv('accounts/LnD-Datasets/Salads.csv')
    allSalads.dropna(inplace = True)
    allSalads.index = np.arange(1, len(allSalads) + 1)
    allSalads.index.name = 'Index'
    allSaladsLength = allSalads.shape[0]


    allMainHP['Main Protein Calories'] = allMainHP['Main Protein'] * 4
    allMainHP['Main Carbs Calories'] = allMainHP['Main Carbs'] * 4
    allMainHP['Main Fats Calories'] = allMainHP['Main Fats'] * 9
    allMainHP['Main Total Calories'] = allMainHP['Main Protein'] * 4 + allMainHP['Main Carbs'] * 4 + allMainHP['Main Fats'] * 9

    allMainLP['Main Protein Calories'] = allMainLP['Main Protein'] * 4
    allMainLP['Main Carbs Calories'] = allMainLP['Main Carbs'] * 4
    allMainLP['Main Fats Calories'] = allMainLP['Main Fats'] * 9
    allMainLP['Main Total Calories'] = allMainLP['Main Protein'] * 4 + allMainLP['Main Carbs'] * 4 + allMainLP['Main Fats'] * 9

    allSides['Sides Protein Calories'] = allSides['Sides Protein'] * 4
    allSides['Sides Carbs Calories'] = allSides['Sides Carbs'] * 4
    allSides['Sides Fats Calories'] = allSides['Sides Fats'] * 9
    allSides['Sides Total Calories'] = allSides['Sides Protein'] * 4 + allSides['Sides Carbs'] * 4 + allSides['Sides Fats'] * 9

    allSalads['Salads Protein Calories'] = allSalads['Salads Protein'] * 4
    allSalads['Salads Carbs Calories'] = allSalads['Salads Carbs'] * 4
    allSalads['Salads Fats Calories'] = allSalads['Salads Fats'] * 9
    allSalads['Salads Total Calories'] = allSalads['Salads Protein'] * 4 + allSalads['Salads Carbs'] * 4 + allSalads['Salads Fats'] * 9

    allMainHP.drop(['Main Protein', 'Main Carbs', 'Main Fats'], axis = 1, inplace = True)
    allMainLP.drop(['Main Protein', 'Main Carbs', 'Main Fats'], axis = 1, inplace = True)
    allSides.drop(['Sides Protein', 'Sides Carbs', 'Sides Fats'], axis = 1, inplace = True)
    allSalads.drop(['Salads Protein', 'Salads Carbs', 'Salads Fats'], axis = 1, inplace = True)


    user_diet = Diet.objects.get(uid = request.user)
    user_profile = Profile.objects.get(uid = request.user)

    if user_profile.food_pref == "veg":
        isVeg =  "Y"
    else:
        isVeg =  "N"
    
    if user_profile.diabetes:
        diabetes = "Y"
    else:
        diabetes = "N"

    if user_profile.thyroid:
        thyroid = "Y"
    else:
        thyroid = "N"

    if user_profile.pcos:
        pcos = "Y"
    else:
        pcos = "N"

    if user_profile.kidney:
        kidney = "Y"
    else:
        kidney = "N"

    if user_profile.lactose:
        lactoseIntolerant = "Y"
    else:
        lactoseIntolerant = "N"
    
    if user_diet.is_vegan:
        vegan = "Y"
    else:
        vegan = "N"
    
    if user_diet.like_salads:
        likeSalads = "Y"
    else:
        likeSalads = "N"
    

    cuisine = ["General"]
    if user_diet.like_north:
        cuisine.append("North Indian")
    
    if user_diet.like_south:
        cuisine.append("South Indian")


    mainHP = copy.deepcopy(allMainHP)
    mainLP = copy.deepcopy(allMainLP)
    sides = copy.deepcopy(allSides)
    salads = copy.deepcopy(allSalads)

    mainHP = mainHP[mainHP['Cuisine (North Indian/ South Indian/ General)'].isin(cuisine)]

    if isVeg == 'Y':
        mainHP = mainHP[mainHP['Type (Veg/ Non Veg)'] == 'Veg']
        mainLP = mainLP[mainLP['Type (Veg/ Non Veg)'] == 'Veg']
        sides = sides[sides['Type (Veg/ Non Veg)'] == 'Veg']
        salads = salads[salads['Type (Veg/ Non Veg)'] == 'Veg']

    if diabetes == 'Y':
        mainHP = mainHP[mainHP['Diabetes'] == 'Y']
        mainLP = mainLP[mainLP['Diabetes'] == 'Y']
        sides = sides[sides['Diabetes'] == 'Y']
        salads = salads[salads['Diabetes'] == 'Y']

    if thyroid == 'Y':
        mainHP = mainHP[mainHP['Thyroid'] == 'Y']
        mainLP = mainLP[mainLP['Thyroid'] == 'Y']
        sides = sides[sides['Thyroid'] == 'Y']
        salads = salads[salads['Thyroid'] == 'Y']

    if pcos == 'Y':
        mainHP = mainHP[mainHP['PCOS'] == 'Y']
        mainLP = mainLP[mainLP['PCOS'] == 'Y']
        sides = sides[sides['PCOS'] == 'Y']
        salads = salads[salads['PCOS'] == 'Y']

    if kidney == 'Y':
        mainHP = mainHP[mainHP['Kidney'] == 'Y']
        mainLP = mainLP[mainLP['Kidney'] == 'Y']
        sides = sides[sides['Kidney'] == 'Y']
        salads = salads[salads['Kidney'] == 'Y']

    if lactoseIntolerant == 'Y':
        mainHP = mainHP[mainHP['Lactose Intolerant'] == 'Y']
        mainLP = mainLP[mainLP['Lactose Intolerant'] == 'Y']
        sides = sides[sides['Lactose Intolerant'] == 'Y']
        salads = salads[salads['Lactose Intolerant'] == 'Y']

    if vegan == 'Y':
        mainHP = mainHP[mainHP['Vegan'] == 'Y']
        mainLP = mainLP[mainLP['Vegan'] == 'Y']
        sides = sides[sides['Vegan'] == 'Y']
        salads = salads[salads['Vegan'] == 'Y']

    mainHP.drop(['Diabetes', 'Thyroid', 'PCOS', 'Kidney', 'Lactose Intolerant', 'Vegan', 'Type (Veg/ Non Veg)',
                'Cuisine (North Indian/ South Indian/ General)'], axis=1, inplace=True)
    mainLP.drop(['Diabetes', 'Thyroid', 'PCOS', 'Kidney', 'Lactose Intolerant', 'Vegan', 'Type (Veg/ Non Veg)',
                'Cuisine (North Indian/ South Indian/ General)'], axis=1, inplace=True)
    sides.drop(['Diabetes', 'Thyroid', 'PCOS', 'Kidney', 'Lactose Intolerant', 'Vegan', 'Type (Veg/ Non Veg)'], axis=1,
            inplace=True)
    salads.drop(['Diabetes', 'Thyroid', 'PCOS', 'Kidney', 'Lactose Intolerant', 'Vegan', 'Type (Veg/ Non Veg)'], axis=1,
                inplace=True)

    mainHPLength = len(mainHP)
    mainLPLength = len(mainLP)
    sidesLength = len(sides)
    saladsLength = len(salads)

    if saladsLength == 0:
        likeSalads = 'N'
        user_diet.like_salads = False
    user_diet.save()

    ldMealHP = mainHP
    ldMealHP = pd.merge(ldMealHP, sides, how='cross')
    if likeSalads == 'Y':
        ldMealHP = pd.merge(ldMealHP, salads, how='cross')

    ldMealHP['Protein Calories'] = ldMealHP['Main Protein Calories'] + ldMealHP['Sides Protein Calories']
    ldMealHP['Carbs Calories'] = ldMealHP['Main Carbs Calories'] + ldMealHP['Sides Carbs Calories']
    ldMealHP['Fats Calories'] = ldMealHP['Main Fats Calories'] + ldMealHP['Sides Fats Calories']
    ldMealHP['Total Calories'] = ldMealHP['Main Total Calories'] + ldMealHP['Sides Total Calories']
    if likeSalads == 'Y':
        ldMealHP['Protein Calories'] += ldMealHP['Salads Protein Calories']
        ldMealHP['Carbs Calories'] += ldMealHP['Salads Carbs Calories']
        ldMealHP['Fats Calories'] += ldMealHP['Salads Fats Calories']
        ldMealHP['Total Calories'] += ldMealHP['Salads Total Calories']

    ldMealHP.index = np.arange(1, len(ldMealHP) + 1)
    ldMealHP.index.name = 'Index'
    ldMealHPLength = ldMealHP.shape[0]


    ldMealLP = mainLP
    ldMealLP = pd.merge(ldMealLP, sides, how='cross')
    if likeSalads == 'Y':
        ldMealLP = pd.merge(ldMealLP, salads, how='cross')

    ldMealLP['Protein Calories'] = ldMealLP['Main Protein Calories'] + ldMealLP['Sides Protein Calories']
    ldMealLP['Carbs Calories'] = ldMealLP['Main Carbs Calories'] + ldMealLP['Sides Carbs Calories']
    ldMealLP['Fats Calories'] = ldMealLP['Main Fats Calories'] + ldMealLP['Sides Fats Calories']
    ldMealLP['Total Calories'] = ldMealLP['Main Total Calories'] + ldMealLP['Sides Total Calories']
    if likeSalads == 'Y':
        ldMealLP['Protein Calories'] += ldMealLP['Salads Protein Calories']
        ldMealLP['Carbs Calories'] += ldMealLP['Salads Carbs Calories']
        ldMealLP['Fats Calories'] += ldMealLP['Salads Fats Calories']
        ldMealLP['Total Calories'] += ldMealLP['Salads Total Calories']

    ldMealLP.index = np.arange(1, len(ldMealLP) + 1)
    ldMealLP.index.name = 'Index'
    ldMealLPLength = ldMealLP.shape[0]


    targetCalories = {'Protein': 0, 'Carbs': 0, 'Fats': 0, 'Total': 0}
    targetCalories['Protein'] = float(user_diet.ld_protein)
    targetCalories['Carbs'] = float(user_diet.ld_carbs)
    targetCalories['Fats'] = float(user_diet.ld_fats)
    targetCalories['Total'] =  targetCalories['Protein'] +  targetCalories['Carbs'] +  targetCalories['Fats']

    ldMealHP['Total Protein Error'] = abs(ldMealHP['Protein Calories'] - targetCalories['Protein'])
    ldMealHP['Total Carbs Error'] = abs(ldMealHP['Carbs Calories'] - targetCalories['Carbs'])
    ldMealHP['Total Fats Error'] = abs(ldMealHP['Fats Calories'] - targetCalories['Fats'])
    ldMealHP['Total Error'] = ldMealHP['Total Protein Error'] + ldMealHP['Total Carbs Error'] + ldMealHP['Total Fats Error']



    selected = {}
    prevLen = -1
    margin = 100
    while len(selected) <= 200 and len(selected) != prevLen and margin <= 250:
        selected = ldMealHP[ldMealHP['Total Error'] <= margin]#[ldMealHP['Total Protein Error'] <= 20][ldMealHP['Total Carbs Error'] <= 30][ldMealHP['Total Fats Error'] <= 20]
        margin += 5
    selected.index = np.arange(1, len(selected) + 1)
    selected.index.name = 'Index'


    lowCarbs = ['Chicken Breast (Raw)', 'Fish', 'Paneer', 'Turkey', 'Skimmed Milk Paneer', 'Low Fat Paneer']
    highCarbs = ['Soya Chunks (Raw)']
    highFats = ['Paneer', 'Low Fat Paneer']
    rice = ['White Rice (Cooked)', 'Brown Rice (Cooked)']
    roti = ['Wheat Roti', 'Bajra Roti']

    selectedLen = len(selected)
    for i in range(1, selectedLen + 1):
        print(i)
        prev = 0
        curr = selected.loc[i]
        counter = 0
        mainRate = 0.05
        sidesRate = 0.03
        saladsRate = 0.02
        while curr.equals(other=prev) == False and counter < 1500:
            prev = copy.deepcopy(curr)
            if curr['Protein Calories'] < 0.95 * targetCalories['Protein']:
                if curr['Main Quantity'] < selected.loc[i, 'Main Quantity'] * 1.6:
                    curr['Main Quantity'] += mainRate * selected.loc[i, 'Main Quantity']
                    curr['Main Protein Calories'] += mainRate * selected.loc[i, 'Main Protein Calories']
                    curr['Main Carbs Calories'] += mainRate * selected.loc[i, 'Main Carbs Calories']
                    curr['Main Fats Calories'] += mainRate * selected.loc[i, 'Main Fats Calories']
                if curr['Sides Quantity'] < selected.loc[i, 'Sides Quantity'] * 1.4:
                    curr['Sides Quantity'] += sidesRate * selected.loc[i, 'Sides Quantity']
                    curr['Sides Protein Calories'] += sidesRate * selected.loc[i, 'Sides Protein Calories']
                    curr['Sides Carbs Calories'] += sidesRate * selected.loc[i, 'Sides Carbs Calories']
                    curr['Sides Fats Calories'] += sidesRate * selected.loc[i, 'Sides Fats Calories']
            if curr['Protein Calories'] > 1.05 * targetCalories['Protein']:
                if curr['Main Quantity'] > selected.loc[i, 'Main Quantity'] * 0.7:
                    curr['Main Quantity'] -= mainRate * selected.loc[i, 'Main Quantity']
                    curr['Main Protein Calories'] -= mainRate * selected.loc[i, 'Main Protein Calories']
                    curr['Main Carbs Calories'] -= mainRate * selected.loc[i, 'Main Carbs Calories']
                    curr['Main Fats Calories'] -= mainRate * selected.loc[i, 'Main Fats Calories']
                if curr['Sides Quantity'] > selected.loc[i, 'Main Quantity'] * 0.6:
                    curr['Sides Quantity'] -= sidesRate * selected.loc[i, 'Sides Quantity']
                    curr['Sides Protein Calories'] -= sidesRate * selected.loc[i, 'Sides Protein Calories']
                    curr['Sides Carbs Calories'] -= sidesRate * selected.loc[i, 'Sides Carbs Calories']
                    curr['Sides Fats Calories'] -= sidesRate * selected.loc[i, 'Sides Fats Calories']

            if curr['Carbs Calories'] < 0.95 * targetCalories['Carbs']:
                if curr['Main Quantity'] < selected.loc[i, 'Main Quantity'] * 1.7 and curr[
                    'Main Name'] in highCarbs and counter % 2:
                    curr['Main Quantity'] += mainRate * selected.loc[i, 'Main Quantity']
                    curr['Main Protein Calories'] += mainRate * selected.loc[i, 'Main Protein Calories']
                    curr['Main Carbs Calories'] += mainRate * selected.loc[i, 'Main Carbs Calories']
                    curr['Main Fats Calories'] += mainRate * selected.loc[i, 'Main Fats Calories']
                if curr['Sides Quantity'] < selected.loc[i, 'Sides Quantity'] * 2:
                    curr['Sides Quantity'] += sidesRate * selected.loc[i, 'Sides Quantity']
                    curr['Sides Protein Calories'] += sidesRate * selected.loc[i, 'Sides Protein Calories']
                    curr['Sides Carbs Calories'] += sidesRate * selected.loc[i, 'Sides Carbs Calories']
                    curr['Sides Fats Calories'] += sidesRate * selected.loc[i, 'Sides Fats Calories']
                if likeSalads == 'Y':
                    if curr['Salads Quantity'] < selected.loc[i, 'Salads Quantity'] * 1.5:
                        curr['Salads Quantity'] += saladsRate * selected.loc[i, 'Salads Quantity']
                        curr['Salads Protein Calories'] += saladsRate * selected.loc[i, 'Salads Protein Calories']
                        curr['Salads Carbs Calories'] += saladsRate * selected.loc[i, 'Salads Carbs Calories']
                        curr['Salads Fats Calories'] += saladsRate * selected.loc[i, 'Salads Fats Calories']

            if curr['Carbs Calories'] > 1.05 * targetCalories['Carbs']:
                if curr['Main Quantity'] > selected.loc[i, 'Main Quantity'] * 0.7 and curr[
                    'Main Name'] in highCarbs and counter % 2:
                    curr['Main Quantity'] -= mainRate * selected.loc[i, 'Main Quantity']
                    curr['Main Protein Calories'] -= mainRate * selected.loc[i, 'Main Protein Calories']
                    curr['Main Carbs Calories'] -= mainRate * selected.loc[i, 'Main Carbs Calories']
                    curr['Main Fats Calories'] -= mainRate * selected.loc[i, 'Main Fats Calories']
                if curr['Sides Quantity'] > selected.loc[i, 'Main Quantity'] * 0.6:
                    curr['Sides Quantity'] -= sidesRate * selected.loc[i, 'Sides Quantity']
                    curr['Sides Protein Calories'] -= sidesRate * selected.loc[i, 'Sides Protein Calories']
                    curr['Sides Carbs Calories'] -= sidesRate * selected.loc[i, 'Sides Carbs Calories']
                    curr['Sides Fats Calories'] -= sidesRate * selected.loc[i, 'Sides Fats Calories']
                if likeSalads == 'Y':
                    if curr['Salads Quantity'] > selected.loc[i, 'Salads Quantity'] * 0.5:
                        curr['Salads Quantity'] -= saladsRate * selected.loc[i, 'Salads Quantity']
                        curr['Salads Protein Calories'] -= saladsRate * selected.loc[i, 'Salads Protein Calories']
                        curr['Salads Carbs Calories'] -= saladsRate * selected.loc[i, 'Salads Carbs Calories']
                        curr['Salads Fats Calories'] -= saladsRate * selected.loc[i, 'Salads Fats Calories']

            if curr['Fats Calories'] < 0.95 * targetCalories['Fats']:
                if curr['Main Quantity'] < selected.loc[i, 'Main Quantity'] * 1.6 and curr['Main Name'] in highFats:
                    curr['Main Quantity'] += mainRate * selected.loc[i, 'Main Quantity']
                    curr['Main Protein Calories'] += mainRate * selected.loc[i, 'Main Protein Calories']
                    curr['Main Carbs Calories'] += mainRate * selected.loc[i, 'Main Carbs Calories']
                    curr['Main Fats Calories'] += mainRate * selected.loc[i, 'Main Fats Calories']
                if curr['Sides Quantity'] < selected.loc[i, 'Sides Quantity'] * 1.4 and curr['Main Name'] in roti:
                    curr['Sides Quantity'] += sidesRate * selected.loc[i, 'Sides Quantity']
                    curr['Sides Protein Calories'] += sidesRate * selected.loc[i, 'Sides Protein Calories']
                    curr['Sides Carbs Calories'] += sidesRate * selected.loc[i, 'Sides Carbs Calories']
                    curr['Sides Fats Calories'] += sidesRate * selected.loc[i, 'Sides Fats Calories']

            if curr['Fats Calories'] > 1.05 * targetCalories['Fats']:
                if curr['Main Quantity'] > selected.loc[i, 'Main Quantity'] * 0.7 and curr['Main Name'] in highFats:
                    curr['Main Quantity'] -= mainRate * selected.loc[i, 'Main Quantity']
                    curr['Main Protein Calories'] -= mainRate * selected.loc[i, 'Main Protein Calories']
                    curr['Main Carbs Calories'] -= mainRate * selected.loc[i, 'Main Carbs Calories']
                    curr['Main Fats Calories'] -= mainRate * selected.loc[i, 'Main Fats Calories']
                if curr['Sides Quantity'] > selected.loc[i, 'Main Quantity'] * 0.6 and curr['Main Name'] in roti:
                    curr['Sides Quantity'] -= sidesRate * selected.loc[i, 'Sides Quantity']
                    curr['Sides Protein Calories'] -= sidesRate * selected.loc[i, 'Sides Protein Calories']
                    curr['Sides Carbs Calories'] -= sidesRate * selected.loc[i, 'Sides Carbs Calories']
                    curr['Sides Fats Calories'] -= sidesRate * selected.loc[i, 'Sides Fats Calories']

            curr['Main Total Calories'] = curr['Main Protein Calories'] + curr['Main Carbs Calories'] + curr[
                'Main Fats Calories']
            curr['Protein Calories'] = curr['Main Protein Calories']
            curr['Carbs Calories'] = curr['Main Carbs Calories']
            curr['Fats Calories'] = curr['Main Fats Calories']
            curr['Sides Total Calories'] = curr['Sides Protein Calories'] + curr['Sides Carbs Calories'] + curr[
                'Sides Fats Calories']
            curr['Protein Calories'] += curr['Sides Protein Calories']
            curr['Carbs Calories'] += curr['Sides Carbs Calories']
            curr['Fats Calories'] += curr['Sides Fats Calories']
            if likeSalads == 'Y':
                curr['Salads Total Calories'] = curr['Salads Protein Calories'] + curr['Salads Carbs Calories'] + curr[
                    'Salads Fats Calories']
                curr['Protein Calories'] += curr['Salads Protein Calories']
                curr['Carbs Calories'] += curr['Salads Carbs Calories']
                curr['Fats Calories'] += curr['Salads Fats Calories']

            curr['Total Calories'] = curr['Protein Calories'] + curr['Carbs Calories'] + curr['Fats Calories']
            curr['Total Protein Error'] = abs(curr['Protein Calories'] - targetCalories['Protein'])
            curr['Total Carbs Error'] = abs(curr['Carbs Calories'] - targetCalories['Carbs'])
            curr['Total Fats Error'] = abs(curr['Fats Calories'] - targetCalories['Fats'])
            curr['Total Error'] = curr['Total Protein Error'] + curr['Total Carbs Error'] + curr['Total Fats Error']

            counter += 1
        selected.loc[i] = curr

    choicesHP = 1
    df1 = {}
    df2 = {}
    prevLen = -1
    proteinMargin = 20
    carbsMargin = 20
    fatsMargin = 20

    while len(df1) <= 20 and prevLen != len(df1) and carbsMargin <= 40 and proteinMargin <= 40:
        df1 = selected.sort_values('Total Error')[selected['Total Carbs Error'] <= carbsMargin][
            selected['Total Fats Error'] <= fatsMargin][selected['Total Protein Error'] <= proteinMargin]
        proteinMargin += 1
        carbsMargin += 1
        fatsMargin += 1

    proteinMargin = 41
    carbsMargin = 20
    fatsMargin = 20

    while len(df2) <= 20 and prevLen != len(df2) and carbsMargin <= 40 and proteinMargin <= 60:
        df2 = selected.sort_values('Total Error')[selected['Total Carbs Error'] <= carbsMargin][
            selected['Total Fats Error'] <= fatsMargin][selected['Total Protein Error'] >= proteinMargin][
            selected['Total Protein Error'] <= 100]
        proteinMargin += 1
        carbsMargin += 1
        fatsMargin += 1

    choicesHP = pd.concat([df1, df2])

    ldMealLP['Total Protein Error'] = abs(ldMealLP['Protein Calories'] - targetCalories['Protein'])
    ldMealLP['Total Carbs Error'] = abs(ldMealLP['Carbs Calories'] - targetCalories['Carbs'])
    ldMealLP['Total Fats Error'] = abs(ldMealLP['Fats Calories'] - targetCalories['Fats'])
    ldMealLP['Total Error'] = ldMealLP['Total Protein Error'] + ldMealLP['Total Carbs Error'] + ldMealLP['Total Fats Error']


    selected = {}
    prevLen = -1
    margin = 100
    while len(selected) <= 200 and len(selected) != prevLen and margin <= 250:
        selected = ldMealLP[ldMealLP['Total Error'] <= margin]#[ldMealLP['Total Protein Error'] <= 20][ldMealLP['Total Carbs Error'] <= 30][ldMealLP['Total Fats Error'] <= 20]
        margin += 5
    selected.index = np.arange(1, len(selected) + 1)
    selected.index.name = 'Index'


    lowCarbs = ['Chicken Breast (Raw)', 'Fish', 'Paneer', 'Turkey', 'Skimmed Milk Paneer', 'Low Fat Paneer']
    highCarbs = ['Soya Chunks (Raw)']
    highFats = ['Kidney Beans (Raw)', 'Low Fat Paneer']
    rice = ['White Rice (Cooked)', 'Brown Rice (Cooked)']
    roti = ['Wheat Roti', 'Bajra Roti']

    selectedLen = len(selected)
    for i in range(1, selectedLen + 1):
        print(i)
        prev = 0
        curr = selected.loc[i]
        counter = 0
        mainRate = 0.05
        sidesRate = 0.03
        saladsRate = 0.02
        while curr.equals(other=prev) == False and counter < 1500:
            prev = copy.deepcopy(curr)
            if curr['Protein Calories'] < 0.95 * targetCalories['Protein']:
                if curr['Main Quantity'] < selected.loc[i, 'Main Quantity'] * 1.6:
                    curr['Main Quantity'] += mainRate * selected.loc[i, 'Main Quantity']
                    curr['Main Protein Calories'] += mainRate * selected.loc[i, 'Main Protein Calories']
                    curr['Main Carbs Calories'] += mainRate * selected.loc[i, 'Main Carbs Calories']
                    curr['Main Fats Calories'] += mainRate * selected.loc[i, 'Main Fats Calories']
                if curr['Sides Quantity'] < selected.loc[i, 'Sides Quantity'] * 1.4:
                    curr['Sides Quantity'] += sidesRate * selected.loc[i, 'Sides Quantity']
                    curr['Sides Protein Calories'] += sidesRate * selected.loc[i, 'Sides Protein Calories']
                    curr['Sides Carbs Calories'] += sidesRate * selected.loc[i, 'Sides Carbs Calories']
                    curr['Sides Fats Calories'] += sidesRate * selected.loc[i, 'Sides Fats Calories']
            if curr['Protein Calories'] > 1.05 * targetCalories['Protein']:
                if curr['Main Quantity'] > selected.loc[i, 'Main Quantity'] * 0.7:
                    curr['Main Quantity'] -= mainRate * selected.loc[i, 'Main Quantity']
                    curr['Main Protein Calories'] -= mainRate * selected.loc[i, 'Main Protein Calories']
                    curr['Main Carbs Calories'] -= mainRate * selected.loc[i, 'Main Carbs Calories']
                    curr['Main Fats Calories'] -= mainRate * selected.loc[i, 'Main Fats Calories']
                if curr['Sides Quantity'] > selected.loc[i, 'Main Quantity'] * 0.6:
                    curr['Sides Quantity'] -= sidesRate * selected.loc[i, 'Sides Quantity']
                    curr['Sides Protein Calories'] -= sidesRate * selected.loc[i, 'Sides Protein Calories']
                    curr['Sides Carbs Calories'] -= sidesRate * selected.loc[i, 'Sides Carbs Calories']
                    curr['Sides Fats Calories'] -= sidesRate * selected.loc[i, 'Sides Fats Calories']

            if curr['Carbs Calories'] < 0.95 * targetCalories['Carbs']:
                if curr['Main Quantity'] < selected.loc[i, 'Main Quantity'] * 1.7:
                    curr['Main Quantity'] += mainRate * selected.loc[i, 'Main Quantity']
                    curr['Main Protein Calories'] += mainRate * selected.loc[i, 'Main Protein Calories']
                    curr['Main Carbs Calories'] += mainRate * selected.loc[i, 'Main Carbs Calories']
                    curr['Main Fats Calories'] += mainRate * selected.loc[i, 'Main Fats Calories']
                if curr['Sides Quantity'] < selected.loc[i, 'Sides Quantity'] * 2:
                    curr['Sides Quantity'] += sidesRate * selected.loc[i, 'Sides Quantity']
                    curr['Sides Protein Calories'] += sidesRate * selected.loc[i, 'Sides Protein Calories']
                    curr['Sides Carbs Calories'] += sidesRate * selected.loc[i, 'Sides Carbs Calories']
                    curr['Sides Fats Calories'] += sidesRate * selected.loc[i, 'Sides Fats Calories']
                if likeSalads == 'Y':
                    if curr['Salads Quantity'] < selected.loc[i, 'Salads Quantity'] * 1.5:
                        curr['Salads Quantity'] += saladsRate * selected.loc[i, 'Salads Quantity']
                        curr['Salads Protein Calories'] += saladsRate * selected.loc[i, 'Salads Protein Calories']
                        curr['Salads Carbs Calories'] += saladsRate * selected.loc[i, 'Salads Carbs Calories']
                        curr['Salads Fats Calories'] += saladsRate * selected.loc[i, 'Salads Fats Calories']

            if curr['Carbs Calories'] > 1.05 * targetCalories['Carbs']:
                if curr['Main Quantity'] > selected.loc[i, 'Main Quantity'] * 0.7:
                    curr['Main Quantity'] -= mainRate * selected.loc[i, 'Main Quantity']
                    curr['Main Protein Calories'] -= mainRate * selected.loc[i, 'Main Protein Calories']
                    curr['Main Carbs Calories'] -= mainRate * selected.loc[i, 'Main Carbs Calories']
                    curr['Main Fats Calories'] -= mainRate * selected.loc[i, 'Main Fats Calories']
                if curr['Sides Quantity'] > selected.loc[i, 'Main Quantity'] * 0.6:
                    curr['Sides Quantity'] -= sidesRate * selected.loc[i, 'Sides Quantity']
                    curr['Sides Protein Calories'] -= sidesRate * selected.loc[i, 'Sides Protein Calories']
                    curr['Sides Carbs Calories'] -= sidesRate * selected.loc[i, 'Sides Carbs Calories']
                    curr['Sides Fats Calories'] -= sidesRate * selected.loc[i, 'Sides Fats Calories']
                if likeSalads == 'Y':
                    if curr['Salads Quantity'] > selected.loc[i, 'Salads Quantity'] * 0.5:
                        curr['Salads Quantity'] -= saladsRate * selected.loc[i, 'Salads Quantity']
                        curr['Salads Protein Calories'] -= saladsRate * selected.loc[i, 'Salads Protein Calories']
                        curr['Salads Carbs Calories'] -= saladsRate * selected.loc[i, 'Salads Carbs Calories']
                        curr['Salads Fats Calories'] -= saladsRate * selected.loc[i, 'Salads Fats Calories']

            if curr['Fats Calories'] < 0.95 * targetCalories['Fats']:
                if curr['Main Quantity'] < selected.loc[i, 'Main Quantity'] * 1.6:
                    curr['Main Quantity'] += mainRate * selected.loc[i, 'Main Quantity']
                    curr['Main Protein Calories'] += mainRate * selected.loc[i, 'Main Protein Calories']
                    curr['Main Carbs Calories'] += mainRate * selected.loc[i, 'Main Carbs Calories']
                    curr['Main Fats Calories'] += mainRate * selected.loc[i, 'Main Fats Calories']
                if curr['Sides Quantity'] < selected.loc[i, 'Sides Quantity'] * 1.4 and curr['Main Name'] in roti:
                    curr['Sides Quantity'] += sidesRate * selected.loc[i, 'Sides Quantity']
                    curr['Sides Protein Calories'] += sidesRate * selected.loc[i, 'Sides Protein Calories']
                    curr['Sides Carbs Calories'] += sidesRate * selected.loc[i, 'Sides Carbs Calories']
                    curr['Sides Fats Calories'] += sidesRate * selected.loc[i, 'Sides Fats Calories']

            if curr['Fats Calories'] > 1.05 * targetCalories['Fats']:
                if curr['Main Quantity'] > selected.loc[i, 'Main Quantity'] * 0.7:
                    curr['Main Quantity'] -= mainRate * selected.loc[i, 'Main Quantity']
                    curr['Main Protein Calories'] -= mainRate * selected.loc[i, 'Main Protein Calories']
                    curr['Main Carbs Calories'] -= mainRate * selected.loc[i, 'Main Carbs Calories']
                    curr['Main Fats Calories'] -= mainRate * selected.loc[i, 'Main Fats Calories']
                if curr['Sides Quantity'] > selected.loc[i, 'Main Quantity'] * 0.6 and curr['Main Name'] in roti:
                    curr['Sides Quantity'] -= sidesRate * selected.loc[i, 'Sides Quantity']
                    curr['Sides Protein Calories'] -= sidesRate * selected.loc[i, 'Sides Protein Calories']
                    curr['Sides Carbs Calories'] -= sidesRate * selected.loc[i, 'Sides Carbs Calories']
                    curr['Sides Fats Calories'] -= sidesRate * selected.loc[i, 'Sides Fats Calories']

            curr['Main Total Calories'] = curr['Main Protein Calories'] + curr['Main Carbs Calories'] + curr[
                'Main Fats Calories']
            curr['Protein Calories'] = curr['Main Protein Calories']
            curr['Carbs Calories'] = curr['Main Carbs Calories']
            curr['Fats Calories'] = curr['Main Fats Calories']
            curr['Sides Total Calories'] = curr['Sides Protein Calories'] + curr['Sides Carbs Calories'] + curr[
                'Sides Fats Calories']
            curr['Protein Calories'] += curr['Sides Protein Calories']
            curr['Carbs Calories'] += curr['Sides Carbs Calories']
            curr['Fats Calories'] += curr['Sides Fats Calories']
            if likeSalads == 'Y':
                curr['Salads Total Calories'] = curr['Salads Protein Calories'] + curr['Salads Carbs Calories'] + curr[
                    'Salads Fats Calories']
                curr['Protein Calories'] += curr['Salads Protein Calories']
                curr['Carbs Calories'] += curr['Salads Carbs Calories']
                curr['Fats Calories'] += curr['Salads Fats Calories']

            curr['Total Calories'] = curr['Protein Calories'] + curr['Carbs Calories'] + curr['Fats Calories']
            curr['Total Protein Error'] = abs(curr['Protein Calories'] - targetCalories['Protein'])
            curr['Total Carbs Error'] = abs(curr['Carbs Calories'] - targetCalories['Carbs'])
            curr['Total Fats Error'] = abs(curr['Fats Calories'] - targetCalories['Fats'])
            curr['Total Error'] = curr['Total Protein Error'] + curr['Total Carbs Error'] + curr['Total Fats Error']

            counter += 1
        selected.loc[i] = curr


    choicesLP = 1
    df1 = {}
    df2 = {}
    prevLen = -1
    proteinMargin = 20
    carbsMargin = 20
    fatsMargin = 20

    while len(df1) <= 20 and prevLen != len(df1) and carbsMargin <= 40 and proteinMargin <= 40:
        df1 = selected.sort_values('Total Error')[selected['Total Carbs Error'] <= carbsMargin][selected['Total Fats Error'] <= fatsMargin][selected['Total Protein Error'] <= proteinMargin]
        proteinMargin += 1
        carbsMargin += 1
        fatsMargin += 1

    proteinMargin = 41
    carbsMargin = 20
    fatsMargin = 20

    while len(df2) <= 20 and prevLen != len(df2) and carbsMargin <= 40 and proteinMargin <= 60:
        df2 = selected.sort_values('Total Error')[selected['Total Carbs Error'] <= carbsMargin][selected['Total Fats Error'] <= fatsMargin][selected['Total Protein Error'] >= proteinMargin][selected['Total Protein Error'] <= 100]
        proteinMargin += 1
        carbsMargin += 1
        fatsMargin += 1

    choicesLP = pd.concat([df1, df2])


    choices = pd.concat([choicesHP, choicesLP])

    while len(choices['Main Name'].unique()) <= 10:
        choices = choices.append(ldMealHP.iloc[random.randint(0, len(ldMealHP) - 1)], ignore_index = True)
        choices = choices.append(ldMealLP.iloc[random.randint(0, len(ldMealLP) - 1)], ignore_index = True)

    choices.index = np.arange(1, len(choices) + 1)
    choices.index.name = 'Index'
    choicesLength = choices.shape[0]

    choices['Protein Powder'] = 0
    for i in range (1, choicesLength + 1):
        if choices.loc[i, "Total Protein Error"] >= 41:
            choices.loc[i, "Protein Powder"] = choices.loc[i, "Total Protein Error"] / 4
        else:
            choices.loc[i, "Protein Powder"] = 0

    finalChoices = []
    al = []
    bl = []
    cl = []
    dl = []
    for j in range(0, 3):
        i = random.randint(1, len(choices))
        aa = choices.loc[i, "Main Name"] + " (" + str(float("{:.2f}".format(choices.loc[i, "Main Quantity"]))) + " g)"
        al.append(aa)
        s = "Main: " + choices.loc[i, "Main Name"] + ", Quantity: " + str(float("{:.2f}".format(choices.loc[i, "Main Quantity"])))
        bb = choices.loc[i, "Sides Name"] + " (" + str(float("{:.2f}".format(choices.loc[i, "Sides Quantity"]))) + " g)"
        bl.append(bb)
        s += "; " + "Side: " + choices.loc[i, "Sides Name"] + ", Quantity: " + str(float("{:.2f}".format(choices.loc[i, "Sides Quantity"])))
        if likeSalads == "Y":
            s += "; " + "Salad: " + choices.loc[i, "Salads Name"] + ", Quantity: " + str(float("{:.2f}".format(choices.loc[i, "Salads Quantity"])))
            cc = choices.loc[i, "Salads Name"] + " (" + str(float("{:.2f}".format(choices.loc[i, "Salads Quantity"]))) + " g)"
            cl.append(cc)
        else:
            cl.append("None")
        s += "; " + "Protein Powder: " + str(float("{:.2f}".format(choices.loc[i, "Protein Powder"])))
        dd = str(float("{:.2f}".format(choices.loc[i, "Protein Powder"]))) + "g"
        dl.append(dd)
        finalChoices.append(s)
    
    finalChoices2 = []
    al2 = []
    bl2 = []
    cl2 = []
    dl2 = []
    print("------------------------------------------------------------")
    print(choices)
    for j in range(0, 3):
        i = random.randint(1, len(choices))
        aa = choices.loc[i, "Main Name"] + " (" + str(float("{:.2f}".format(choices.loc[i, "Main Quantity"]))) + " g)"
        al2.append(aa)
        s = "Main: " + choices.loc[i, "Main Name"] + ", Quantity: " + str(float("{:.2f}".format(choices.loc[i, "Main Quantity"])))
        bb = choices.loc[i, "Sides Name"] + " (" + str(float("{:.2f}".format(choices.loc[i, "Sides Quantity"]))) + " g)"
        bl2.append(bb)
        s += "; " + "Side: " + choices.loc[i, "Sides Name"] + ", Quantity: " + str(float("{:.2f}".format(choices.loc[i, "Sides Quantity"])))
        if likeSalads == "Y":
            s += "; " + "Salad: " + choices.loc[i, "Salads Name"] + ", Quantity: " + str(float("{:.2f}".format(choices.loc[i, "Salads Quantity"])))
            cc = choices.loc[i, "Salads Name"] + " (" + str(float("{:.2f}".format(choices.loc[i, "Salads Quantity"]))) + " g)"
            cl2.append(cc)
        else:
            cl2.append("None")
        s += "; " + "Protein Powder: " + str(float("{:.2f}".format(choices.loc[i, "Protein Powder"])))
        dd = str(float("{:.2f}".format(choices.loc[i, "Protein Powder"]))) + "g"
        dl2.append(dd)
        finalChoices2.append(s)


    user_lunch = Lunch.objects.get(uid = request.user)
    user_lunch.l_main_1 = al[0]
    user_lunch.l_main_2 = al[1]
    user_lunch.l_main_3 = al[2]
    user_lunch.l_side_1 = bl[0]
    user_lunch.l_side_2 = bl[1]
    user_lunch.l_side_3 = bl[2]
    user_lunch.l_salad_1 = cl[0]
    user_lunch.l_salad_2 = cl[1]
    user_lunch.l_salad_3 = cl[2]
    user_lunch.l_pp_1 = dl[0]
    user_lunch.l_pp_2 = dl[1]
    user_lunch.l_pp_3 = dl[2]
    choices = choices.to_json()
    user_lunch.choices = json.dumps(choices)
    user_lunch.save()

    user_dinner = Dinner.objects.get(uid = request.user)
    user_dinner.d_main_1 = al2[0]
    user_dinner.d_main_2 = al2[1]
    user_dinner.d_main_3 = al2[2]
    user_dinner.d_side_1 = bl2[0]
    user_dinner.d_side_2 = bl2[1]
    user_dinner.d_side_3 = bl2[2]
    user_dinner.d_salad_1 = cl2[0]
    user_dinner.d_salad_2 = cl2[1]
    user_dinner.d_salad_3 = cl2[2]
    user_dinner.d_pp_1 = dl2[0]
    user_dinner.d_pp_2 = dl2[1]
    user_dinner.d_pp_3 = dl2[2]
    user_dinner.choices = json.dumps(choices)
    user_dinner.save()
    
    context = {"dest":"snacks_api"}
    return render(request,"loading_diet.html", context)

def snacks_api(request):
    import copy
    import pandas as pd
    import numpy as np
    import random

    user_diet = Diet.objects.get(uid = request.user)
    allSnacks = pd.read_csv('accounts/Snack-Datasets/Snacks.csv')
    allSnacks.dropna(inplace = True)
    allSnacks.index = np.arange(1, len(allSnacks) + 1)
    allSnacks.index.name = 'Index'
    allSnacksLength = allSnacks.shape[0]

    allFruits = pd.read_csv('accounts/Snack-Datasets/Fruits.csv')
    allFruits.dropna(inplace = True)
    allFruits.index = np.arange(1, len(allFruits) + 1)
    allFruits.index.name = 'Index'
    allFruitsLength = allFruits.shape[0]

    allSweets = pd.read_csv('accounts/Snack-Datasets/Sweets.csv')
    allSweets.dropna(inplace = True)
    allSweets.index = np.arange(1, len(allSweets) + 1)
    allSweets.index.name = 'Index'
    allSweetsLength = allSweets.shape[0]


    allSnacks['Snacks Calories'] = allSnacks['Snacks Protein'] * 4 + allSnacks['Snacks Carbs'] * 4 + allSnacks['Snacks Fats'] * 9
    allFruits['Fruits Calories'] = allFruits['Fruits Protein'] * 4 + allFruits['Fruits Carbs'] * 4 + allFruits['Fruits Fats'] * 9
    allSweets['Sweets Calories'] = allSweets['Sweets Protein'] * 4 + allSweets['Sweets Carbs'] * 4 + allSweets['Sweets Fats'] * 9


    user_diet = Diet.objects.get(uid = request.user)
    user_profile = Profile.objects.get(uid = request.user)

    if user_profile.food_pref == "veg":
        isVeg =  "Y"
    else:
        isVeg =  "N"
    
    if user_profile.diabetes:
        diabetes = "Y"
    else:
        diabetes = "N"

    if user_profile.thyroid:
        thyroid = "Y"
    else:
        thyroid = "N"

    if user_profile.pcos:
        pcos = "Y"
    else:
        pcos = "N"

    if user_profile.kidney:
        kidney = "Y"
    else:
        kidney = "N"

    if user_profile.lactose:
        lactoseIntolerant = "Y"
    else:
        lactoseIntolerant = "N"
    
    if user_diet.is_vegan:
        vegan = "Y"
    else:
        vegan = "N"

    if user_diet.like_fruits:
        likeFruits = "Y"
    else:
        likeFruits = "N"
    
    if user_diet.like_sweets:
        likeSweets = "Y"
    else:
        likeSweets = "N"

    snacks = copy.deepcopy(allSnacks)
    fruits = copy.deepcopy(allFruits)
    sweets = copy.deepcopy(allSweets)

    if isVeg == 'Y':
        snacks = snacks[snacks['Type (Veg/ Non Veg)'] == 'Veg']
        fruits = fruits[fruits['Type (Veg/ Non Veg)'] == 'Veg']
        sweets = sweets[sweets['Type (Veg/ Non Veg)'] == 'Veg']

    if diabetes == 'Y':
        snacks = snacks[snacks['Diabetes'] == 'Y']
        fruits = fruits[fruits['Diabetes'] == 'Y']
        sweets = sweets[sweets['Diabetes'] == 'Y']

    if thyroid == 'Y':
        snacks = snacks[snacks['Thyroid'] == 'Y']
        fruits = fruits[fruits['Thyroid'] == 'Y']
        sweets = sweets[sweets['Thyroid'] == 'Y']

    if pcos == 'Y':
        snacks = snacks[snacks['PCOS'] == 'Y']
        fruits = fruits[fruits['PCOS'] == 'Y']
        sweets = sweets[sweets['PCOS'] == 'Y']

    if kidney == 'Y':
        snacks = snacks[snacks['Kidney'] == 'Y']
        fruits = fruits[fruits['Kidney'] == 'Y']
        sweets = sweets[sweets['Kidney'] == 'Y']

    if lactoseIntolerant == 'Y':
        snacks = snacks[snacks['Lactose Intolerant'] == 'Y']
        fruits = fruits[fruits['Lactose Intolerant'] == 'Y']
        sweets = sweets[sweets['Lactose Intolerant'] == 'Y']

    if vegan == 'Y':
        snacks = snacks[snacks['Vegan'] == 'Y']
        fruits = fruits[fruits['Vegan'] == 'Y']
        sweets = sweets[sweets['Vegan'] == 'Y']

    snacks.drop(
        ['Diabetes', 'Thyroid', 'PCOS', 'Kidney', 'Lactose Intolerant', 'Vegan', 'Type (Veg/ Non Veg)', 'Snacks Protein',
        'Snacks Carbs', 'Snacks Fats', 'Snacks Fibre'], axis=1, inplace=True)
    fruits.drop(
        ['Diabetes', 'Thyroid', 'PCOS', 'Kidney', 'Lactose Intolerant', 'Vegan', 'Type (Veg/ Non Veg)', 'Fruits Protein',
        'Fruits Carbs', 'Fruits Fats', 'Fruits Fibre'], axis=1, inplace=True)
    sweets.drop(
        ['Diabetes', 'Thyroid', 'PCOS', 'Kidney', 'Lactose Intolerant', 'Vegan', 'Type (Veg/ Non Veg)', 'Sweets Protein',
        'Sweets Carbs', 'Sweets Fats', 'Sweets Fibre'], axis=1, inplace=True)
    

    snacksLength = snacks.shape[0]
    fruitsLength = fruits.shape[0]
    sweetsLength = sweets.shape[0]

    if fruitsLength == 0:
        likeFruits = 'N'
        user_diet.like_fruits = False
    if sweetsLength == 0:
        likeSweets = 'N'
        user_diet.like_sweets = False
    user_diet.save()

    snacksMeal = snacks
    if likeFruits == 'Y':
        snacksMeal = pd.merge(snacksMeal, fruits, how='cross')

    if likeSweets == 'Y':
        snacksMeal = pd.merge(snacksMeal, sweets, how='cross')

    snacksMeal['Total Calories'] = snacksMeal['Snacks Calories']
    if likeFruits == 'Y':
        snacksMeal['Total Calories'] += snacksMeal['Fruits Calories']
    if likeSweets == 'Y':
        snacksMeal['Total Calories'] += snacksMeal['Sweets Calories']


    targetCalories = float(user_diet.snack_calories)
    snacksMeal['Total Error'] = abs(snacksMeal['Total Calories'] - targetCalories)

    selected = snacksMeal.sort_values('Total Error')[snacksMeal['Total Error'] <= 200]
    selected.index = np.arange(1, len(selected) + 1)
    selected.index.name = 'Index'

    selectedLen = len(selected)
    for i in range(1, selectedLen + 1):
        print(i)
        prev = 0
        curr = selected.loc[i]
        counter = 0
        snacksRate = 0.05
        fruitsRate = 0.03
        sweetsRate = 0.02
        while curr.equals(other=prev) == False and counter < 500:
            prev = copy.deepcopy(curr)
            if curr['Total Calories'] < 0.95 * targetCalories:
                if curr['Snacks Quantity'] < selected.loc[i, 'Snacks Quantity'] * 1.8:
                    curr['Snacks Quantity'] += snacksRate * selected.loc[i, 'Snacks Quantity']
                    curr['Snacks Calories'] += snacksRate * selected.loc[i, 'Snacks Calories']
                if likeFruits == 'Y':
                    if curr['Fruits Quantity'] < selected.loc[i, 'Fruits Quantity'] * 1.5:
                        curr['Fruits Quantity'] += fruitsRate * selected.loc[i, 'Fruits Quantity']
                        curr['Fruits Calories'] += fruitsRate * selected.loc[i, 'Fruits Calories']
                if likeSweets == 'Y':
                    if curr['Sweets Quantity'] < selected.loc[i, 'Sweets Quantity'] * 1.5:
                        curr['Sweets Quantity'] += sweetsRate * selected.loc[i, 'Sweets Quantity']
                        curr['Sweets Calories'] += sweetsRate * selected.loc[i, 'Sweets Calories']

            if curr['Total Calories'] > 1.05 * targetCalories:
                if curr['Snacks Quantity'] > selected.loc[i, 'Snacks Quantity'] * 0.5:
                    curr['Snacks Quantity'] -= snacksRate * selected.loc[i, 'Snacks Quantity']
                    curr['Snacks Calories'] -= snacksRate * selected.loc[i, 'Snacks Calories']
                if likeFruits == 'Y':
                    if curr['Fruits Quantity'] > selected.loc[i, 'Fruits Quantity'] * 0.5:
                        curr['Fruits Quantity'] -= fruitsRate * selected.loc[i, 'Fruits Quantity']
                        curr['Fruits Calories'] -= fruitsRate * selected.loc[i, 'Fruits Calories']
                if likeSweets == 'Y':
                    if curr['Sweets Quantity'] > selected.loc[i, 'Sweets Quantity'] * 0.5:
                        curr['Sweets Quantity'] -= sweetsRate * selected.loc[i, 'Sweets Quantity']
                        curr['Sweets Calories'] -= sweetsRate * selected.loc[i, 'Sweets Calories']

            curr['Total Calories'] = curr['Snacks Calories']
            if likeFruits == 'Y':
                curr['Total Calories'] += curr['Fruits Calories']
            if likeSweets == 'Y':
                curr['Total Calories'] += curr['Sweets Calories']
            curr['Total Error'] = abs(curr['Total Calories'] - targetCalories)

            counter += 1
        selected.loc[i] = curr


    choices = selected[selected['Total Error'] < 20]

    choices.index = np.arange(1, len(choices) + 1)
    choices.index.name = 'Index'
    choicesLength = choices.shape[0]
    al = []
    bl = []
    cl = []
    for j in range(0, 3):
        i = random.randint(1, len(choices))
        aa = ""
        bb = ""
        cc = ""
        aa += choices.loc[i, "Snacks Name"] + " (" + str(float("{:.2f}".format(choices.loc[i, "Snacks Quantity"]))) + " g )"
        al.append(aa)
        if likeFruits == "Y":
            bb +=  choices.loc[i, "Fruits Name"] + " (" + str(float("{:.2f}".format(choices.loc[i, "Fruits Quantity"]))) + " g )"
            bl.append(bb)
        else:
            bb += "NONE"
            bl.append(bb)
        
        if likeSweets == "Y":
            cc +=  choices.loc[i, "Sweets Name"] + " (" + str(float("{:.2f}".format(choices.loc[i, "Sweets Quantity"]))) + " g )"
            cl.append(cc)
        else:
            cc += "NONE"
            cl.append(cc)

    user_snack = Snacks.objects.get(uid = request.user)
    user_snack.s_main_1 = al[0]
    user_snack.s_main_2 = al[1]
    user_snack.s_main_3 = al[2]
    user_snack.s_fruit_1 = bl[0]
    user_snack.s_fruit_2 = bl[1]
    user_snack.s_fruit_3 = bl[2]
    user_snack.s_sweet_1 = cl[0]
    user_snack.s_sweet_2 = cl[1]
    user_snack.s_sweet_3 = cl[2]
    choices = choices.to_json()
    user_snack.choices = json.dumps(choices)
    user_snack.save()

    context = {'dest': "diet_disp"}
    return render(request, "loading_diet.html",context)

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
        context = {'dest': "bf_api"}
        return render(request, "loading_diet.html",context)
    else:
        user_diet = Diet.objects.get(uid = request.user)
        context = {"user_diet":user_diet}
        return render(request, 'diet-qn.html', context)

def view_diet(request):
    user_diet = Diet.objects.get(uid = request.user)
    if user_diet.plan_exists:
        user_bf = Breakfast.objects.get(uid = request.user)
        user_lunch = Lunch.objects.get(uid = request.user)
        user_dinner = Dinner.objects.get(uid= request.user)
        user_snacks = Snacks.objects.get(uid = request.user)
        context = {'user_bf': user_bf, 'user_lunch': user_lunch, 'user_dinner': user_dinner, 'user_snacks':user_snacks} 
        return render(request, "diet2.html", context)
    else:
        user_diet = Diet.objects.get(uid = request.user)
        context = {"user_diet":user_diet}
        return redirect('/diet', context)


def regenerate(request):
    if request.method == "GET":
        import pandas as pd
        user_diet = Diet.objects.get(uid = request.user)
        user_lunch = Lunch.objects.get(uid=request.user)
        user_snack = Snacks.objects.get(uid = request.user)
        user_bf = Breakfast.objects.get(uid = request.user)
        user_dinner = Dinner.objects.get(uid = request.user)

        cuisine = ["General"]
        if user_diet.like_north:
            cuisine.append("North Indian")
        
        if user_diet.like_south:
            cuisine.append("South Indian")
        #----------------------------SNACKS-------------------------------------
        
        if user_diet.like_fruits:
            likeFruits = "Y"
        else:
            likeFruits = "N"
        
        if user_diet.like_sweets:
            likeSweets = "Y"
        else:
            likeSweets = "N"
        
        
        
        choices1 = json.loads(user_snack.choices)
        choices1 = pd.read_json(choices1)
        print("REGENERATE--------------------------------------------")
        print(choices1)
        asn = []
        bsn = []
        csn = []
        for j in range(0, 3):
            i = random.randint(1, len(choices1))
            aa = choices1.loc[i, "Snacks Name"] + " (" + str(float("{:.2f}".format(choices1.loc[i, "Snacks Quantity"]))) + " g )"
            asn.append(aa)
            if likeFruits == "Y":
                bb =  choices1.loc[i, "Fruits Name"] + " (" + str(float("{:.2f}".format(choices1.loc[i, "Fruits Quantity"]))) + " g )"
                bsn.append(bb)
            else:
                bb = "NONE"
                bsn.append(bb)
            
            if likeSweets == "Y":
                cc =  choices1.loc[i, "Sweets Name"] + " (" + str(float("{:.2f}".format(choices1.loc[i, "Sweets Quantity"]))) + " g )"
                csn.append(cc)
            else:
                cc = "NONE"
                csn.append(cc)
        
        user_snack.s_main_1 = asn[0]
        user_snack.s_main_2 = asn[1]
        user_snack.s_main_3 = asn[2]
        user_snack.s_fruit_1 = bsn[0]
        user_snack.s_fruit_2 = bsn[1]
        user_snack.s_fruit_3 = bsn[2]
        user_snack.s_sweet_1 = csn[0]
        user_snack.s_sweet_2 = csn[1]
        user_snack.s_sweet_3 = csn[2]
        user_snack.save()
        
        #----------------------------LUNCH & DINNER-----------------------------
       
        if user_diet.like_salads:
            likeSalads = "Y"
        else:
            likeSalads = "N"
        
        choices2 = json.loads(user_lunch.choices)
        choices2 = pd.read_json(choices2)

        finalChoices = []
        al = []
        bl = []
        cl = []
        dl = []
        for j in range(0, 3):
            i = random.randint(1, len(choices2))
            aa = choices2.loc[i, "Main Name"] + " (" + str(float("{:.2f}".format(choices2.loc[i, "Main Quantity"]))) + " g)"
            al.append(aa)
            s = "Main: " + choices2.loc[i, "Main Name"] + ", Quantity: " + str(float("{:.2f}".format(choices2.loc[i, "Main Quantity"])))
            bb = choices2.loc[i, "Sides Name"] + " (" + str(float("{:.2f}".format(choices2.loc[i, "Sides Quantity"]))) + " g)"
            bl.append(bb)
            s += "; " + "Side: " + choices2.loc[i, "Sides Name"] + ", Quantity: " + str(float("{:.2f}".format(choices2.loc[i, "Sides Quantity"])))
            if likeSalads == "Y":
                s += "; " + "Salad: " + choices2.loc[i, "Salads Name"] + ", Quantity: " + str(float("{:.2f}".format(choices2.loc[i, "Salads Quantity"])))
                cc = choices2.loc[i, "Salads Name"] + " (" + str(float("{:.2f}".format(choices2.loc[i, "Salads Quantity"]))) + " g)"
                cl.append(cc)
            else:
                cl.append("None")
            s += "; " + "Protein Powder: " + str(float("{:.2f}".format(choices2.loc[i, "Protein Powder"])))
            dd = str(float("{:.2f}".format(choices2.loc[i, "Protein Powder"]))) + "g"
            dl.append(dd)
            finalChoices.append(s)
        
        finalChoices2 = []
        al2 = []
        bl2 = []
        cl2 = []
        dl2 = []
        print("------------------------------------------------------------")
        print(choices2)
        for j in range(0, 3):
            i = random.randint(1, len(choices2))
            aa = choices2.loc[i, "Main Name"] + " (" + str(float("{:.2f}".format(choices2.loc[i, "Main Quantity"]))) + " g)"
            al2.append(aa)
            s = "Main: " + choices2.loc[i, "Main Name"] + ", Quantity: " + str(float("{:.2f}".format(choices2.loc[i, "Main Quantity"])))
            bb = choices2.loc[i, "Sides Name"] + " (" + str(float("{:.2f}".format(choices2.loc[i, "Sides Quantity"]))) + " g)"
            bl2.append(bb)
            s += "; " + "Side: " + choices2.loc[i, "Sides Name"] + ", Quantity: " + str(float("{:.2f}".format(choices2.loc[i, "Sides Quantity"])))
            if likeSalads == "Y":
                s += "; " + "Salad: " + choices2.loc[i, "Salads Name"] + ", Quantity: " + str(float("{:.2f}".format(choices2.loc[i, "Salads Quantity"])))
                cc = choices2.loc[i, "Salads Name"] + " (" + str(float("{:.2f}".format(choices2.loc[i, "Salads Quantity"]))) + " g)"
                cl2.append(cc)
            else:
                cl2.append("None")
            s += "; " + "Protein Powder: " + str(float("{:.2f}".format(choices2.loc[i, "Protein Powder"])))
            dd = str(float("{:.2f}".format(choices2.loc[i, "Protein Powder"]))) + "g"
            dl2.append(dd)
            finalChoices2.append(s)

        user_lunch.l_main_1 = al[0]
        user_lunch.l_main_2 = al[1]
        user_lunch.l_main_3 = al[2]
        user_lunch.l_side_1 = bl[0]
        user_lunch.l_side_2 = bl[1]
        user_lunch.l_side_3 = bl[2]
        user_lunch.l_salad_1 = cl[0]
        user_lunch.l_salad_2 = cl[1]
        user_lunch.l_salad_3 = cl[2]
        user_lunch.l_pp_1 = dl[0]
        user_lunch.l_pp_2 = dl[1]
        user_lunch.l_pp_3 = dl[2]
        user_lunch.save()

        user_dinner.d_main_1 = al2[0]
        user_dinner.d_main_2 = al2[1]
        user_dinner.d_main_3 = al2[2]
        user_dinner.d_side_1 = bl2[0]
        user_dinner.d_side_2 = bl2[1]
        user_dinner.d_side_3 = bl2[2]
        user_dinner.d_salad_1 = cl2[0]
        user_dinner.d_salad_2 = cl2[1]
        user_dinner.d_salad_3 = cl2[2]
        user_dinner.d_pp_1 = dl2[0]
        user_dinner.d_pp_2 = dl2[1]
        user_dinner.d_pp_3 = dl2[2]
        user_dinner.save()

        #-----------------------------BREAKFAST---------------------------------
        
        if user_diet.like_milk:
            likeMilk = "Y"
        else:
            likeMilk = "N"
        
        if user_diet.like_fruits:
            likeFruits = "Y"
        else:
            likeFruits = "N"

        if user_diet.like_seeds_nuts:
            likeNuts = "Y"
        else:
            likeNuts = "N"
        
        choices3 = json.loads(user_bf.choices)
        choices3 = pd.read_json(choices3)
        
        finalChoices = []
        abf = []
        bbf = []
        cbf = []
        dbf = []
        ebf =[]
        for j in range(0, 3):
            print("CHECKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK")
            i = random.randint(1, len(choices3))
            s = "Main: " + choices3.loc[i, "Breakfast Name"] + ", Quantity: " + str(float("{:.2f}".format(choices3.loc[i, "Breakfast Quantity"])))
            aa = choices3.loc[i, "Breakfast Name"] + " (" + str(float("{:.2f}".format(choices3.loc[i, "Breakfast Quantity"]))) + " g)"
            abf.append(aa)
            if likeMilk == "Y":
                s += "; " + "Milk: " + choices3.loc[i, "Milk Name"] + ", Quantity: " + str(float("{:.2f}".format(choices3.loc[i, "Milk Quantity"])))
                bb = choices3.loc[i, "Milk Name"] + " (" + str(float("{:.2f}".format(choices3.loc[i, "Milk Quantity"]))) + " g)"
                bbf.append(bb)
            else:
                bbf.append("None")
            if likeFruits == "Y":
                s += "; " + "Fruit: " + choices3.loc[i, "Fruits Name"] + ", Quantity: " + str(float("{:.2f}".format(choices3.loc[i, "Fruits Quantity"])))
                cc = choices3.loc[i, "Fruits Name"] + " (" + str(float("{:.2f}".format(choices3.loc[i, "Fruits Quantity"]))) + " g)"
                cbf.append(cc)
            else:
                cbf.append("None")
            if likeNuts == "Y":
                s += "; " + "Nut: " + choices3.loc[i, "Nuts Name"] + ", Quantity: " + str(float("{:.2f}".format(choices3.loc[i, "Nuts Quantity"])))
                dd = choices3.loc[i, "Nuts Name"] + " (" + str(float("{:.2f}".format(choices3.loc[i, "Nuts Quantity"]))) + " g)"
                dbf.append(dd)
            else:
                dbf.append("None")
            s += "; " + "Protein Powder: " + str(float("{:.2f}".format(choices3.loc[i, "Protein Powder"])))
            ee = str(float("{:.2f}".format(choices3.loc[i, "Protein Powder"]))) + " g"
            ebf.append(ee)
            finalChoices.append(s)
        print(finalChoices)
        user_bf = Breakfast.objects.get(uid = request.user)
        print("ABF: ", abf)
        user_bf.bf_main_1 = abf[0]
        user_bf.bf_main_2 = abf[1]
        user_bf.bf_main_3 = abf[2]
        user_bf.bf_milk_1 = bbf[0]
        user_bf.bf_milk_2 = bbf[1]
        user_bf.bf_milk_3 = bbf[2]
        user_bf.bf_fruits_1 = cbf[0]
        user_bf.bf_fruits_2 = cbf[1]
        user_bf.bf_fruits_3 = cbf[2]
        user_bf.bf_nuts_1 = dbf[0]
        user_bf.bf_nuts_2 = dbf[1]
        user_bf.bf_nuts_3 = dbf[2]
        user_bf.bf_pp_1 = ebf[0]
        user_bf.bf_pp_2 = ebf[1]
        user_bf.bf_pp_3 = ebf[2]
        user_bf.save()

    context = {'dest': "diet_disp"}
    return render(request, "loading_diet.html",context)