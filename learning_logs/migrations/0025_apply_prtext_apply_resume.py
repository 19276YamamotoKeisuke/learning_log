# Generated by Django 4.0.4 on 2023-01-06 15:08

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('learning_logs', '0024_entry_address_entry_selection_method'),
    ]

    operations = [
        migrations.AddField(
            model_name='apply',
            name='PRtext',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='apply',
            name='resume',
            field=models.FileField(default=django.utils.timezone.now, upload_to='resume/'),
            preserve_default=False,
        ),
    ]
