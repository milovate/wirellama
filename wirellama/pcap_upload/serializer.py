from rest_framework import serializers
from .models import PCAPFile

from rest_framework import serializers
from .models import PacketData

class PacketDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = PacketData
        fields = [
            'id',
            'frame_number',
            'frame_time',
            'frame_len',
            'eth_src',
            'eth_dst',
            'eth_type',
            'ip_src',
            'ip_dst',
            'ip_proto',
            'ip_ttl',
            'tcp_srcport',
            'tcp_dstport',
            'tcp_flags',
            'tcp_seq',
            'udp_srcport',
            'udp_dstport',
            'udp_length',
            'http_request_method',
            'http_response_code',
            'http_host',
            'dns_qry_name',
            'dns_resp_name',
            'dns_flags_response',
            
        ]