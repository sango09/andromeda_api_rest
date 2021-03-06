# Generated by Django 3.0.11 on 2021-02-18 19:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('assistant', '0002_assistant_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('technical_support', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='support',
            name='request_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='ratingsupport',
            name='rated_assistant',
            field=models.ForeignKey(help_text='Auxiliar que recibe la calificación', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rated_assistant', to='assistant.Assistant'),
        ),
        migrations.AddField(
            model_name='ratingsupport',
            name='rating_user',
            field=models.ForeignKey(help_text='Usuario que califica el soporte tecnico', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rating_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='ratingsupport',
            name='support',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rated_support', to='technical_support.Support'),
        ),
    ]
