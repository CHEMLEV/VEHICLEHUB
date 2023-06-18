# Generated by Django 4.2 on 2023-06-17 21:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('VehicleHub', '0029_vehiclemake'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vehicle',
            name='make',
        ),
        migrations.AddField(
            model_name='vehicle',
            name='brand',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='VehicleHub.vehiclemake'),
            preserve_default=False,
        ),
    ]
