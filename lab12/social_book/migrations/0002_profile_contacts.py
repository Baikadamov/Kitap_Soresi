# Generated by Django 4.1.7 on 2023-04-26 12:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_book', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='contacts',
            field=models.TextField(blank=True),
        ),
    ]
