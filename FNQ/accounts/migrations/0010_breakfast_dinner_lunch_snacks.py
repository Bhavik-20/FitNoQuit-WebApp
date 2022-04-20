# Generated by Django 3.2.11 on 2022-04-15 06:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('accounts', '0009_rename_wo_plan_workout_sug_wo_cal_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Breakfast',
            fields=[
                ('uid', models.ForeignKey(db_column='uid', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='auth.user')),
                ('bf_main_1', models.CharField(max_length=50)),
                ('bf_main_2', models.CharField(max_length=50)),
                ('bf_main_3', models.CharField(max_length=50)),
                ('bf_milk_1', models.CharField(max_length=50)),
                ('bf_milk_2', models.CharField(max_length=50)),
                ('bf_milk_3', models.CharField(max_length=50)),
                ('bf_fruits_1', models.CharField(max_length=50)),
                ('bf_fruits_2', models.CharField(max_length=50)),
                ('bf_fruits_3', models.CharField(max_length=50)),
                ('bf_nuts_1', models.CharField(max_length=50)),
                ('bf_nuts_2', models.CharField(max_length=50)),
                ('bf_nuts_3', models.CharField(max_length=50)),
                ('bf_pp_1', models.CharField(max_length=50)),
                ('bf_pp_2', models.CharField(max_length=50)),
                ('bf_pp_3', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Dinner',
            fields=[
                ('uid', models.ForeignKey(db_column='uid', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='auth.user')),
                ('d_main_1', models.CharField(max_length=50)),
                ('d_main_2', models.CharField(max_length=50)),
                ('d_main_3', models.CharField(max_length=50)),
                ('d_side_1', models.CharField(max_length=50)),
                ('d_side_2', models.CharField(max_length=50)),
                ('d_side_3', models.CharField(max_length=50)),
                ('d_salad_1', models.CharField(max_length=50)),
                ('d_salad_2', models.CharField(max_length=50)),
                ('d_salad_3', models.CharField(max_length=50)),
                ('d_pp_1', models.CharField(max_length=50)),
                ('d_pp_2', models.CharField(max_length=50)),
                ('d_pp_3', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Lunch',
            fields=[
                ('uid', models.ForeignKey(db_column='uid', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='auth.user')),
                ('l_main_1', models.CharField(max_length=50)),
                ('l_main_2', models.CharField(max_length=50)),
                ('l_main_3', models.CharField(max_length=50)),
                ('l_side_1', models.CharField(max_length=50)),
                ('l_side_2', models.CharField(max_length=50)),
                ('l_side_3', models.CharField(max_length=50)),
                ('l_salad_1', models.CharField(max_length=50)),
                ('l_salad_2', models.CharField(max_length=50)),
                ('l_salad_3', models.CharField(max_length=50)),
                ('l_pp_1', models.CharField(max_length=50)),
                ('l_pp_2', models.CharField(max_length=50)),
                ('l_pp_3', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Snacks',
            fields=[
                ('uid', models.ForeignKey(db_column='uid', on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='auth.user')),
                ('s_main_1', models.CharField(max_length=50)),
                ('s_main_2', models.CharField(max_length=50)),
                ('s_main_3', models.CharField(max_length=50)),
                ('s_fruit_1', models.CharField(max_length=50)),
                ('s_fruit_2', models.CharField(max_length=50)),
                ('s_fruit_3', models.CharField(max_length=50)),
                ('s_sweet_1', models.CharField(max_length=50)),
                ('s_sweet_2', models.CharField(max_length=50)),
                ('s_sweet_3', models.CharField(max_length=50)),
            ],
        ),
    ]
