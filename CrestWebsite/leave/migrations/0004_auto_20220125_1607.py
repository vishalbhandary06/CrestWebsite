# Generated by Django 3.2.9 on 2022-01-25 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leave', '0003_auto_20220125_1553'),
    ]

    operations = [
        migrations.AlterField(
            model_name='remaining_leaves',
            name='casual_leave',
            field=models.IntegerField(default=20),
        ),
        migrations.AlterField(
            model_name='remaining_leaves',
            name='sick_leave',
            field=models.IntegerField(default=5),
        ),
    ]
