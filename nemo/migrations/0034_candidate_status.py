# Generated by Django 4.2 on 2023-06-02 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nemo', '0033_alter_candidate_birth_month'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='status',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
