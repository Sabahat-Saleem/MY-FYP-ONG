# Generated by Django 5.1.6 on 2025-03-11 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('add_user', '0003_remove_user_name_alter_user_first_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('season', models.CharField(choices=[('Winter', 'Winter'), ('Spring', 'Spring'), ('Summer', 'Summer'), ('Autumn', 'Autumn')], max_length=10)),
                ('travel_type', models.CharField(choices=[('Adventure', 'Adventure'), ('Relaxation', 'Relaxation'), ('Cultural', 'Cultural'), ('Wildlife', 'Wildlife')], max_length=15)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('season', models.CharField(choices=[('Winter', 'Winter'), ('Spring', 'Spring'), ('Summer', 'Summer'), ('Autumn', 'Autumn')], max_length=10)),
                ('travel_type', models.CharField(choices=[('Adventure', 'Adventure'), ('Relaxation', 'Relaxation'), ('Cultural', 'Cultural'), ('Wildlife', 'Wildlife')], max_length=15)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='TravelTip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('season', models.CharField(blank=True, choices=[('Winter', 'Winter'), ('Spring', 'Spring'), ('Summer', 'Summer'), ('Autumn', 'Autumn')], max_length=10, null=True)),
                ('travel_type', models.CharField(blank=True, choices=[('Adventure', 'Adventure'), ('Relaxation', 'Relaxation'), ('Cultural', 'Cultural'), ('Wildlife', 'Wildlife')], max_length=15, null=True)),
                ('content', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='preferred_season',
            field=models.CharField(blank=True, choices=[('Winter', 'Winter'), ('Spring', 'Spring'), ('Summer', 'Summer'), ('Autumn', 'Autumn')], max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='preferred_travel_type',
            field=models.CharField(blank=True, choices=[('Adventure', 'Adventure'), ('Relaxation', 'Relaxation'), ('Cultural', 'Cultural'), ('Wildlife', 'Wildlife')], max_length=15, null=True),
        ),
    ]
