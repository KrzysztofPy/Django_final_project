# Generated by Django 3.2.12 on 2022-03-28 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointment_app', '0008_auto_20220326_1132'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='physicianspeciality',
            name='speciality',
        ),
        migrations.AddField(
            model_name='physicianspeciality',
            name='specialities',
            field=models.IntegerField(choices=[(0, '---'), (1, 'Internal medicine'), (2, 'Pediatrician'), (3, 'Family medicine'), (4, 'Dermatologist'), (5, 'Cardiologist'), (6, 'Endocrinologist'), (7, 'Gastroenterologist'), (8, 'Neurologist'), (9, 'Urologist'), (10, 'Radiologist'), (11, 'Orthopaedist')], default=1),
            preserve_default=False,
        ),
    ]
