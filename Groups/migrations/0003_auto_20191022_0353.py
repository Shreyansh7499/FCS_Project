# Generated by Django 2.2.5 on 2019-10-21 22:23

from django.conf import settings
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Groups', '0002_auto_20191022_0350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='date_posted',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='members',
            field=models.ManyToManyField(blank=True, null=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='group',
            name='message',
            field=models.TextField(blank=True, max_length=100, null=True),
        ),
    ]