# Generated by Django 4.2 on 2023-06-02 07:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('nemo', '0037_alter_documenttype_document_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='group',
            field=models.CharField(choices=[('OFFICER', 'OFFICER'), ('RATING', 'RATING'), ('IV CREW', 'IV CREW')], default=1, max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='candidate',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='candidate',
            name='vendor',
            field=models.CharField(default=django.utils.timezone.now, max_length=200),
            preserve_default=False,
        ),
    ]
