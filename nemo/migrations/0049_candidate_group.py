# Generated by Django 4.2 on 2023-06-02 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nemo', '0048_alter_candidate_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='group',
            field=models.CharField(choices=[('OFFICER', 'OFFICER'), ('RATING', 'RATING'), ('IV CREW', 'IV CREW')], default=1, max_length=200),
            preserve_default=False,
        ),
    ]
