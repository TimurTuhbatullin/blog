# Generated by Django 4.1 on 2023-04-06 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learning_logs', '0003_topic_verified'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='verified',
            field=models.BooleanField(default=False),
        ),
    ]
