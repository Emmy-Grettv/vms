# Generated by Django 5.1.3 on 2024-11-21 20:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('events', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstName', models.CharField(max_length=200)),
                ('lastName', models.CharField(max_length=200)),
                ('userType', models.PositiveIntegerField(choices=[(0, '-----'), (1, 'Volunteer'), (2, 'Organizer')], default=0)),
                ('userName', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, to_field='username')),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orgName', models.CharField(max_length=50)),
                ('orgDivision', models.CharField(max_length=50)),
                ('orgRating', models.PositiveIntegerField(default=0)),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='volunteers.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Volunteer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skills', models.CharField(max_length=500)),
                ('highLevelEducation', models.CharField(max_length=30)),
                ('event', models.ManyToManyField(to='events.event')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='volunteers.profile')),
            ],
        ),
    ]