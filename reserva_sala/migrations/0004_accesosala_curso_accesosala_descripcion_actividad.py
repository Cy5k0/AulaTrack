# Generated by Django 5.1.6 on 2025-03-05 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reserva_sala', '0003_alter_accesosala_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='accesosala',
            name='curso',
            field=models.CharField(blank=True, help_text='Indique el curso con el que asistirá', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='accesosala',
            name='descripcion_actividad',
            field=models.TextField(blank=True, help_text='Describa brevemente la actividad a realizar', null=True),
        ),
    ]
