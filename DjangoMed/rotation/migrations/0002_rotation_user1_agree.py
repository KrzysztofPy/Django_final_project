# Generated by Django 3.2.12 on 2022-04-06 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rotation', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='rotation',
            name='user1_agree',
            field=models.BooleanField(default=False),
        ),
    ]
