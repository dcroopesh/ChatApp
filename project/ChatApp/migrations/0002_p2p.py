# Generated by Django 2.2 on 2020-04-03 13:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ChatApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='p2p',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=30)),
                ('roomname', models.CharField(max_length=10)),
                ('send_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent', to=settings.AUTH_USER_MODEL)),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
