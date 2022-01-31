# Generated by Django 3.2.11 on 2022-01-28 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_profile_uid'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='email',
            field=models.EmailField(default=None, max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='fname',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='lname',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
    ]