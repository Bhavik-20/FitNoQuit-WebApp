# Generated by Django 4.0 on 2022-05-01 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0005_alter_blogs_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogs',
            name='img',
            field=models.ImageField(upload_to='blog_images/'),
        ),
    ]
