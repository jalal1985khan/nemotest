# Generated by Django 4.2 on 2023-05-29 08:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nemo', '0028_candidate_date_rem_alter_countryname_country_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='candidate',
            old_name='date_rem',
            new_name='birth_remainder',
        ),
    ]
