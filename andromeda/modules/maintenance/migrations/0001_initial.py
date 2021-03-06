# Generated by Django 3.0.11 on 2021-02-18 19:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('assistant', '0001_initial'),
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Maintenance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Fecha y hora del registro', verbose_name='creado el')),
                ('modified', models.DateTimeField(auto_now=True, help_text='Fecha y hora de la ultima modificación', verbose_name='modificado el')),
                ('auxiliary_id', models.IntegerField(null=True)),
                ('image_implement', models.ImageField(blank=True, default='inventory/pictures/default-image.png', null=True, upload_to='maintenance/pictures')),
                ('maintenance_location', models.CharField(help_text='Lugar del mantenimiento', max_length=50)),
                ('event_google_id', models.CharField(max_length=100, null=True)),
                ('maintenance_date', models.DateTimeField()),
                ('maintenance_type', models.CharField(max_length=50)),
                ('complete_maintenance_date', models.DateTimeField(blank=True, null=True)),
                ('description', models.TextField()),
                ('is_active', models.BooleanField(default=True, help_text='Se utiliza para marcar cuando el mantenimiento fue completado o cancelado', verbose_name='estado de activo')),
                ('assigned_auxiliary', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='assistant.Assistant')),
                ('implement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.Inventory')),
            ],
            options={
                'db_table': 'tbl_mantenimientos',
            },
        ),
    ]
