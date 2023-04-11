# Generated by Django 4.1 on 2023-04-09 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learning_logs', '0007_entry_views'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='entry',
            name='views',
        ),
        migrations.AddField(
            model_name='topic',
            name='views',
            field=models.PositiveIntegerField(default=0),
        ),
    ]