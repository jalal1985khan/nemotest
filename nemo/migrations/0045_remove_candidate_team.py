# Generated by Django 4.2 on 2023-06-02 09:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nemo', '0044_rename_active_candidate_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='candidate',
            name='team',
        ),
    ]
