from django.db import models

# Create your models here.

class PCAPFile(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    pcap_file = models.FileField(upload_to='pcap_files', null=True, blank=True)
    json_file = models.FileField(upload_to='json_files', null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class PacketData(models.Model):
    frame_number = models.CharField(max_length=50,  null=True, blank=True)
    frame_time = models.CharField(max_length=100, null=True, blank=True)
    frame_len = models.IntegerField(null=True, blank=True)
    eth_src = models.CharField(max_length=50, null=True, blank=True)
    eth_dst = models.CharField(max_length=50, null=True, blank=True)
    eth_type = models.CharField(max_length=50, null=True, blank=True)
    ip_src = models.CharField(max_length=50, null=True, blank=True)
    ip_dst = models.CharField(max_length=50, null=True, blank=True)
    ip_proto = models.CharField(max_length=50, null=True, blank=True)
    ip_ttl = models.IntegerField(null=True, blank=True)
    tcp_srcport = models.IntegerField(null=True, blank=True)
    tcp_dstport = models.IntegerField(null=True, blank=True)
    tcp_flags = models.CharField(max_length=50, null=True, blank=True)
    tcp_seq = models.BigIntegerField(null=True, blank=True)
    udp_srcport = models.IntegerField(null=True, blank=True)
    udp_dstport = models.IntegerField(null=True, blank=True)
    udp_length = models.IntegerField(null=True, blank=True)
    http_request_method = models.CharField(max_length=50, null=True, blank=True)
    http_response_code = models.IntegerField(null=True, blank=True)
    http_host = models.CharField(max_length=100, null=True, blank=True)
    dns_qry_name = models.CharField(max_length=100, null=True, blank=True)
    dns_resp_name = models.CharField(max_length=100, null=True, blank=True)
    dns_flags_response = models.CharField(max_length=50, null=True, blank=True)
   
    def __str__(self):
        return f"Packet {self.frame_number} from {self.ip_src} to {self.ip_dst}"
