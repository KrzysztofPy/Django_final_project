# Generated by Django 3.2.12 on 2022-03-26 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointment_app', '0007_auto_20220326_1038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='rating',
            field=models.IntegerField(blank=True, choices=[(0, '*'), (1, '**'), (2, '***'), (3, '****'), (4, '*****')], null=True),
        ),
        migrations.AlterField(
            model_name='physicianspeciality',
            name='speciality',
            field=models.IntegerField(choices=[(-1, '---'), (0, 'Internal medicine'), (1, 'Pediatrician'), (2, 'Family medicine'), (3, 'Dermatologist'), (4, 'Cardiologist'), (5, 'Endocrinologist'), (6, 'Gastroenterologist'), (7, 'Neurologist'), (8, 'Urologist'), (9, 'Radiologist'), (10, 'Orthopaedist')]),
        ),
    ]