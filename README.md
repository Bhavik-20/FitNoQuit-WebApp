# FitNoQuit-WebApp
BTech Final Year Project

In today’s fast-paced world, it is not uncommon for people to experience mental and physical illness. Various scientific studies have shown that a wholesome diet and any form of physical activity helps in relieving health issues and progress towards a healthy lifestyle both physically and mentally. However, not everyone has the appropriate knowledge to help them reach their fitness goal. Thus we developed a Diet and Workout recommendation system named  “FitNoQuit”, that is developed using Machine Learning. FitNoQuit takes into account various parameters like height, weight, age and then calculates the current BMI & BMR of the user, food preferences like vegetarian/Non-vegetarian/Vegan, and chronic health conditions like diabetes, PCOS, thyroid, etc. Based on these user inputs the system provides a nutritional diet and workout plan which enables the user to reach his/her end fitness goal.

# Introduction

FitNoQuit has 3 primary features:
1. **Diet Recommendation**: The system considers user inputs such as height, weight, age, diseases, food preferences, end goal etc to generate a personalized diet using machine learning algorithm. The diet consists of meals and foods that best suits the user and will help him/her to achieve their end goal.
2. **Workout Recommendation**: The system suggests workouts to user using mathematical computations and compliments with diet recommended to impact the overall calorie management of the user. The user is given options with respect to the time he/she wishes to dedicate for the workout along with 
workout options they prefer. The workouts aren’t recommended to elder users as they might have existing physical conditions like joint pain and arthritis which may need supervision.
3. **Blog suggestions**: FitNoQuit offers a blog section to its users wherein they can select categories of blogs they wish to read. This section aims at keeping the users abreast with the current fitness trends and updates. With the help of collaborative and/or content-based filtering, users will be recommended blogs based on their interest and likings.

Steps to access the website:
* New users must sign up to the application to access its features. All users can access the blogs section.
* Before accessing the diet and workout recommendation features of the web app the users must complete their profile.
* After completing their profile the users should be able to access their diet recommendations. 
* Once diet recommendations are made, the user can access their workout recommendations and track their progress.

<!-- ![Steps](/readme-contents/Steps.png =20x) -->
<img src="readme-contents/Steps.png " width="600">

# Tools and Database
* Django Framework
* PostgreSQL as Database

# Getting Started
---------- You can skip the installation of this project and directly access it [here](https://fit-no-quit.herokuapp.com/) ----------

Follow the steps for project installation:
1. Clone repository from GitHub using following url:
```
https://github.com/Bhavik-20/FitNoQuit-WebApp.git
```
2. Download & Install Visual Studio Code on the machine. [Windows](https://www.youtube.com/watch?v=JPZsB_6yHVo), [Mac](https://www.youtube.com/watch?v=8CJXB4Nu1wo)
3. Download & Install Python on the machine and add it to environment variables. [Windows](https://www.youtube.com/watch?v=RAFZleZYxsc), [Mac](https://www.youtube.com/watch?v=5AOkxqFaYEE)
4. Download & Install Django on the machine using “pip install django” command.
5. Download & Install PostgreSQL and PgAdmin for database connectivity.
6. Create and configure a new database with the following credentials (available in 
FNQ/settings.py)
7. Install the following python packages and dependencies using “pip install”
command
    - Django==4.0
    - django-heroku==0.3.1
    - gunicorn==20.1.0
    - argcomplete==1.12.3
    - argon2-cffi==21.1.0
    - asgiref==3.4.1
    - debugpy==1.4.3
    - jedi==0.18.0
    - Jinja2==3.0.1
    - joblib==1.1.0
    - jsonschema==3.2.0
    - nest-asyncio==1.5.1
    - nltk==3.6.5
    - notebook==6.4.3
    - numpy==1.21.2
    - packaging==21.0
    - pandas==1.3.3
    - pandocfilters==1.5.0
    - Pillow==8.3.2
    - psycopg2==2.9.3
    - py3dns==3.2.1
    - pycparser==2.20
    - Pygments==2.10.0
    - pyparsing==2.4.7
    - pyrsistent==0.18.0
    - pytz==2021.1
    - regex==2021.10.23
    - scikit-learn==1.0
    - six==1.16.0
    - sklearn==0.0
    - sqlparse==0.4.2
    - validate-email-address==1
    - whitenoise==6.0.0
8. Make migrations to the database using “python manage.py migrate”.
9. Execute the project using “python manage.py runserver”.
10. The server will start running after executing the statement in step 9 and the
application would be accessible in the following url:
```
 http://127.0.0.1:8000/ 
```

