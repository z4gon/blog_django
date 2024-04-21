# Generated by Django 4.2.11 on 2024-04-20 22:00

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0013_alter_author_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='bookmarkers',
            field=models.ManyToManyField(blank=True, related_name='bookmarks', to=settings.AUTH_USER_MODEL),
        ),
    ]