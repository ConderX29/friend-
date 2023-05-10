# Generated by Django 4.2.1 on 2023-05-10 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('friends', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='friend',
            name='users',
        ),
        migrations.AddField(
            model_name='friend',
            name='sers',
            field=models.ManyToManyField(related_name='friendships', to='friends.user'),
        ),
        migrations.AddField(
            model_name='friendrequest',
            name='accepted',
            field=models.BooleanField(default=False),
        ),
    ]
