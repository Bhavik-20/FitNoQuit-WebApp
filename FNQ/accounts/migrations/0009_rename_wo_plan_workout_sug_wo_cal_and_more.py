# Generated by Django 4.0 on 2022-03-27 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_workout_weight'),
    ]

    operations = [
        migrations.RenameField(
            model_name='workout',
            old_name='wo_plan',
            new_name='sug_wo_cal',
        ),
        migrations.AddField(
            model_name='workout',
            name='sug_wo_categories',
            field=models.TextField(default=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='workout',
            name='sug_wo_name',
            field=models.TextField(default=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='workout',
            name='sug_wo_time',
            field=models.TextField(default=200),
            preserve_default=False,
        ),
    ]