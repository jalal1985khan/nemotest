# Generated by Django 4.2 on 2023-05-23 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nemo', '0026_notifications_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='port',
            name='port_name',
            field=models.CharField(max_length=200, null=True, unique=True),
        ),
    ]