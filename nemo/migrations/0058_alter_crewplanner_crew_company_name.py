# Generated by Django 4.2 on 2023-06-05 05:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nemo', '0057_alter_crewplanner_crew_rank'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crewplanner',
            name='crew_company_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='nemo.company'),
        ),
    ]
