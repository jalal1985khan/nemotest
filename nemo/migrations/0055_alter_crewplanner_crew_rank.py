# Generated by Django 4.2 on 2023-06-05 05:48

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('nemo', '0054_alter_crewplanner_crew_immediate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crewplanner',
            name='crew_rank',
            field=models.ForeignKey(default=django.utils.timezone.now, on_delete=django.db.models.deletion.CASCADE, to='nemo.rank'),
            preserve_default=False,
        ),
    ]