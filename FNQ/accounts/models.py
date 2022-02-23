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
    bmi = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    fitness_goal = models.CharField(max_length=20)
    curr_exercise = models.CharField(max_length=50)
    food_pref = models.CharField(max_length=10)
    diabetes = models.BooleanField(default=False)
    thyroid = models.BooleanField(default=False)
    pcos = models.BooleanField(default=False)
    kidney = models.BooleanField(default=False)
    lactose = models.BooleanField(default=False)


