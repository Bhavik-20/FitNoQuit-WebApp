# Generated by Django 3.2.11 on 2022-03-25 09:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blogs',
            fields=[
                ('blog_id', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=50)),
                ('category', models.CharField(max_length=20)),
                ('author', models.CharField(max_length=20)),
                ('publish_date', models.DateField()),
                ('content', models.CharField(max_length=1000)),
                ('img', models.CharField(max_length=100)),
            ],
        ),
    ]