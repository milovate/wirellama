# Generated by Django 5.0.6 on 2024-07-03 22:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pcap_upload', '0002_alter_pcapfile_json_data'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pcapfile',
            name='file',
        ),
        migrations.RemoveField(
            model_name='pcapfile',
            name='json_data',
        ),
        migrations.AddField(
            model_name='pcapfile',
            name='json_file',
            field=models.FileField(blank=True, null=True, upload_to='json_files'),
        ),
        migrations.AddField(
            model_name='pcapfile',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='pcapfile',
            name='pcap_file',
            field=models.FileField(blank=True, null=True, upload_to='pcap_files'),
        ),
        migrations.CreateModel(
            name='PacketData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('frame_number', models.CharField(blank=True, max_length=50, null=True)),
                ('frame_time', models.CharField(blank=True, max_length=100, null=True)),
                ('frame_len', models.IntegerField(blank=True, null=True)),
                ('eth_src', models.CharField(blank=True, max_length=50, null=True)),
                ('eth_dst', models.CharField(blank=True, max_length=50, null=True)),
                ('eth_type', models.CharField(blank=True, max_length=50, null=True)),
                ('ip_src', models.CharField(blank=True, max_length=50, null=True)),
                ('ip_dst', models.CharField(blank=True, max_length=50, null=True)),
                ('ip_proto', models.CharField(blank=True, max_length=50, null=True)),
                ('ip_ttl', models.IntegerField(blank=True, null=True)),
                ('tcp_srcport', models.IntegerField(blank=True, null=True)),
                ('tcp_dstport', models.IntegerField(blank=True, null=True)),
                ('tcp_flags', models.CharField(blank=True, max_length=50, null=True)),
                ('tcp_seq', models.BigIntegerField(blank=True, null=True)),
                ('udp_srcport', models.IntegerField(blank=True, null=True)),
                ('udp_dstport', models.IntegerField(blank=True, null=True)),
                ('udp_length', models.IntegerField(blank=True, null=True)),
                ('http_request_method', models.CharField(blank=True, max_length=50, null=True)),
                ('http_response_code', models.IntegerField(blank=True, null=True)),
                ('http_host', models.CharField(blank=True, max_length=100, null=True)),
                ('dns_qry_name', models.CharField(blank=True, max_length=100, null=True)),
                ('dns_resp_name', models.CharField(blank=True, max_length=100, null=True)),
                ('dns_flags_response', models.CharField(blank=True, max_length=50, null=True)),
                ('pcap_file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='packet_data', to='pcap_upload.pcapfile')),
            ],
        ),
    ]
