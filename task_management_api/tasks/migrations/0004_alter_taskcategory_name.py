# Generated by Django 5.1 on 2024-09-29 01:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_task_is_completed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskcategory',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
