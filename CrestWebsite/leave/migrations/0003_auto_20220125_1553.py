# Generated by Django 3.2.9 on 2022-01-25 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leave', '0002_remaining_leaves'),
    ]

    operations = [
        migrations.AddField(
            model_name='remaining_leaves',
            name='casual_leave',
            field=models.CharField(default=20, max_length=3),
        ),
        migrations.AddField(
            model_name='remaining_leaves',
            name='sick_leave',
            field=models.CharField(default=5, max_length=3),
        ),
    ]
