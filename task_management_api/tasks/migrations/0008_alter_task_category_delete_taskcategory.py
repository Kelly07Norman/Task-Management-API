# Generated by Django 5.1 on 2024-10-01 02:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0001_initial'),
        ('tasks', '0007_alter_task_category_alter_task_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='categories.taskcategory'),
        ),
        migrations.DeleteModel(
            name='TaskCategory',
        ),
    ]
