# Generated by Django 5.1.6 on 2025-03-06 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('add_user', '0002_user_mobile_number_alter_user_name_dashboard'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='name',
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=70),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=70),
        ),
    ]
