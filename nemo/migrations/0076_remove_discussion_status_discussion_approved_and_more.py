# Generated by Django 4.2 on 2023-06-20 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nemo', '0075_rename_refernce_discussion_reminder_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='discussion',
            name='status',
        ),
        migrations.AddField(
            model_name='discussion',
            name='approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='discussion',
            name='joined',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='discussion',
            name='proposed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='discussion',
            name='rejected',
            field=models.BooleanField(default=False),
        ),
    ]
