# Generated by Django 4.2 on 2023-05-29 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nemo', '0032_candidate_birth_month'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='birth_month',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
