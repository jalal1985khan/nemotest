# Generated by Django 4.2 on 2023-06-20 10:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nemo', '0074_alter_discussion_comment_check_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='discussion',
            old_name='refernce',
            new_name='reminder_date',
        ),
    ]
