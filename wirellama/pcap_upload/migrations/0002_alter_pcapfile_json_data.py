# Generated by Django 5.0.6 on 2024-07-03 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pcap_upload', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pcapfile',
            name='json_data',
            field=models.JSONField(null=True),
        ),
    ]
