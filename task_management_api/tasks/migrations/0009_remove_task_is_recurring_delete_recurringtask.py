# Generated by Django 5.1 on 2024-10-06 17:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0008_alter_task_category_delete_taskcategory'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='is_recurring',
        ),
        migrations.DeleteModel(
            name='RecurringTask',
        ),
    ]
