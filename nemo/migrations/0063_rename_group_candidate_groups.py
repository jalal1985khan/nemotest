# Generated by Django 4.2 on 2023-06-05 16:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nemo', '0062_medical'),
    ]

    operations = [
        migrations.RenameField(
            model_name='candidate',
            old_name='group',
            new_name='groups',
        ),
    ]
