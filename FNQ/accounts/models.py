from django.db import models
from django.contrib.auth.models import User, auth

# Create your models here.

class Profile(models.Model):
    uid = models.ForeignKey(User, on_delete=models.CASCADE, primary_key= True, db_column='uid') 
    fname = models.CharField(max_length=20)
    lname = models.CharField(max_length=20)
    email = models.EmailField()
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10)
    height = models.DecimalField(max_digits=4, decimal_places=1)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    start_wt = models.DecimalField(max_digits=5, decimal_places=2)
    target_wt = models.DecimalField(max_digits=5, decimal_places=2)
    bmi = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    fitness_goal = models.CharField(max_length=20)
    curr_exercise = models.CharField(max_length=50)
    food_pref = models.CharField(max_length=10)
    diabetes = models.BooleanField(default=False)
    thyroid = models.BooleanField(default=False)
    pcos = models.BooleanField(default=False)
    kidney = models.BooleanField(default=False)
    lactose = models.BooleanField(default=False)

class Diet(models.Model):
    uid = models.ForeignKey(User, on_delete=models.CASCADE, primary_key= True, db_column='uid')
    diet_calories = models.PositiveBigIntegerField()
    plan_exists =  models.BooleanField(default=False)
    is_vegan = models.BooleanField(default= False)
    like_milk = models.BooleanField(default=True)
    like_seeds_nuts = models.BooleanField(default=True)
    like_sweets = models.BooleanField(default=True)
    like_fruits = models.BooleanField(default=True)
    like_salads = models.BooleanField(default=True)
    like_north = models.BooleanField(default=True)
    like_south = models.BooleanField(default=True)
    bf_protein = models.DecimalField(max_digits=5, decimal_places=2)
    bf_carbs = models.DecimalField(max_digits=5, decimal_places=2)
    bf_fats = models.DecimalField(max_digits=5, decimal_places=2)
    ld_protein = models.DecimalField(max_digits=5, decimal_places=2)
    ld_carbs = models.DecimalField(max_digits=5, decimal_places=2)
    ld_fats = models.DecimalField(max_digits=5, decimal_places=2)
    snack_calories = models.DecimalField(max_digits=5, decimal_places=2)
  

class Breakfast(models.Model):
    uid = models.ForeignKey(User, on_delete=models.CASCADE, primary_key= True, db_column='uid')
    bf_main_1 = models.CharField(max_length=50, default= "None")
    bf_main_2 = models.CharField(max_length=50, default= "None")
    bf_main_3 = models.CharField(max_length=50, default= "None")
    bf_milk_1 = models.CharField(max_length=50, default= "None")
    bf_milk_2 = models.CharField(max_length=50, default= "None")
    bf_milk_3 = models.CharField(max_length=50, default= "None")
    bf_fruits_1 = models.CharField(max_length=50, default= "None")
    bf_fruits_2 = models.CharField(max_length=50, default= "None")
    bf_fruits_3 = models.CharField(max_length=50, default= "None")
    bf_nuts_1 = models.CharField(max_length=50, default= "None")
    bf_nuts_2 = models.CharField(max_length=50, default= "None")
    bf_nuts_3 = models.CharField(max_length=50, default= "None")
    bf_pp_1 = models.CharField(max_length=50, default= "None")
    bf_pp_2 = models.CharField(max_length=50, default= "None")
    bf_pp_3 = models.CharField(max_length=50, default= "None")
    choices = models.TextField()
    
class Lunch(models.Model):
    uid = models.ForeignKey(User, on_delete=models.CASCADE, primary_key= True, db_column='uid')
    l_main_1 = models.CharField(max_length=50, default= "None")
    l_main_2 = models.CharField(max_length=50, default= "None")
    l_main_3 = models.CharField(max_length=50, default= "None")
    l_side_1 = models.CharField(max_length=50, default= "None")
    l_side_2 = models.CharField(max_length=50, default= "None")
    l_side_3 = models.CharField(max_length=50, default= "None")
    l_salad_1 = models.CharField(max_length=50, default= "None")
    l_salad_2 = models.CharField(max_length=50, default= "None")
    l_salad_3 = models.CharField(max_length=50, default= "None")
    l_pp_1 = models.CharField(max_length=50, default= "None")
    l_pp_2 = models.CharField(max_length=50, default= "None")
    l_pp_3 = models.CharField(max_length=50, default= "None")
    choices = models.TextField()

class Dinner(models.Model):
    uid = models.ForeignKey(User, on_delete=models.CASCADE, primary_key= True, db_column='uid')
    d_main_1 = models.CharField(max_length=50, default= "None")
    d_main_2 = models.CharField(max_length=50, default= "None")
    d_main_3 = models.CharField(max_length=50, default= "None")
    d_side_1 = models.CharField(max_length=50, default= "None")
    d_side_2 = models.CharField(max_length=50, default= "None")
    d_side_3 = models.CharField(max_length=50, default= "None")
    d_salad_1 = models.CharField(max_length=50, default= "None")
    d_salad_2 = models.CharField(max_length=50, default= "None")
    d_salad_3 = models.CharField(max_length=50, default= "None")
    d_pp_1 = models.CharField(max_length=50, default= "None")
    d_pp_2 = models.CharField(max_length=50, default= "None")
    d_pp_3 = models.CharField(max_length=50, default= "None")
    choices = models.TextField()

class Snacks(models.Model):
    uid = models.ForeignKey(User, on_delete=models.CASCADE, primary_key= True, db_column='uid')
    s_main_1 = models.CharField(max_length=50, default= "None")
    s_main_2 = models.CharField(max_length=50, default= "None")
    s_main_3 = models.CharField(max_length=50, default= "None")
    s_fruit_1 = models.CharField(max_length=50, default= "None")
    s_fruit_2 = models.CharField(max_length=50, default= "None")
    s_fruit_3 = models.CharField(max_length=50, default= "None")
    s_sweet_1 = models.CharField(max_length=50, default= "None")
    s_sweet_2 = models.CharField(max_length=50, default= "None")
    s_sweet_3 = models.CharField(max_length=50, default= "None")
    choices = models.TextField()
    
class Workout(models.Model):
    uid = models.ForeignKey(User, on_delete=models.CASCADE, primary_key= True, db_column='uid')
    wo_exists =  models.BooleanField(default=False)
    wo_calories = models.PositiveBigIntegerField()
    time = models.CharField(max_length=500,default= "None")
    wo_type = models.CharField(max_length=500, default= "None")
    sug_wo_name = models.TextField(default= "None") 
    sug_wo_categories = models.TextField(default= "None") 
    sug_wo_time = models.TextField(default= "None")  
    sug_wo_cal = models.TextField(default= "None")     
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    