# Generated by Django 4.2 on 2023-05-29 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nemo', '0027_alter_port_port_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='date_rem',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='countryname',
            name='country_name',
            field=models.CharField(max_length=200, null=True, unique=True),
        ),
    ]
