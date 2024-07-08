
# Create your views here.
from django.shortcuts import render
import os
import json
from django.conf import settings
from django.http import JsonResponse
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView
from .models import PacketData
from .serializer import PacketDataSerializer
from scapy.all import rdpcap
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import subprocess
from django.core.exceptions import ValidationError
from llama_agents.launchers.local import LocalLauncher
from llama_agents.services import AgentService, ToolService
from llama_agents.tools import MetaServiceTool
from llama_agents.control_plane.server import ControlPlaneServer
from llama_agents.message_queues.simple import SimpleMessageQueue
from llama_agents.orchestrators.agent import AgentOrchestrator

from llama_index.core.agent import FunctionCallingAgentWorker
from llama_index.core.tools import FunctionTool
from llama_index.llms.openai import OpenAI
from llama_index.core import Settings
from time import sleep
from IPython.display import Markdown, display
from llama_index.core import SQLDatabase
from llama_index.core import Settings
from llama_index.llms.together import TogetherLLM
from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    String,
    Integer,
    select,
)
import nest_asyncio



class CHATView(APIView):
    
    
    def post(self, request, format=None):
        print(request.data)
        
        with open('/home/milind/linux-github/wirellama/wirellama/pcap_upload/message.txt', 'w') as file:
            file.write(request.data["message"])
            # Run tllamatest.py after saving the message
        
        subprocess.run(["python3", "/home/milind/linux-github/wirellama/wirellama/pcap_upload/tllamatest.py"]) 
        sleep(1)     
        with open('/home/milind/linux-github/wirellama/wirellama/pcap_upload/output.txt', 'r') as file:
            output = file.read()
        
        return JsonResponse({'message': output}, status=200)




class PCAPUploadView(APIView):
    parser_classes = [MultiPartParser]
    
    @classmethod
    def run_tshark(self,pcap_file, output_file):
        
        command = [
            "tshark",
            "-r", pcap_file,
            "-T", "json",
            "-e", "frame.number",
            "-e", "frame.time",
            "-e", "frame.len",
            "-e", "eth.src",
            "-e", "eth.dst",
            "-e", "eth.type",
            "-e", "ip.src",
            "-e", "ip.dst",
            "-e", "ip.proto",
            "-e", "ip.ttl",
            "-e", "tcp.srcport",
            "-e", "tcp.dstport",
            "-e", "tcp.flags",
            "-e", "tcp.seq",
            "-e", "udp.srcport",
            "-e", "udp.dstport",
            "-e", "udp.length",
            "-e", "http.request.method",
            "-e", "http.response.code",
            "-e", "http.host",
            "-e", "dns.qry.name",
            "-e", "dns.resp.name",
            "-e", "dns.flags.response"
        ]

        result = subprocess.run(command, capture_output=True, text=True, check=True)
        
        # Parse the JSON output
        packets = json.loads(result.stdout)
            

        # Extract only the 'layers' part from each packet
        layers_only = [packet['_source']['layers'] for packet in packets]

        # Adjust the output_file path to save in media/json_files
        output_file = os.path.join('media', 'json_files', os.path.basename(output_file))

        # Ensure the directory exists
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        # Save the extracted layers to the adjusted file path
        with open(output_file, 'w') as f:
            json.dump(layers_only, f, indent=2)


    
    # Save the packet data to the database
    def save_packet_data(self, json_file_path):
        
        with open(json_file_path, 'r') as file:
            packet_data_list = json.load(file)
            
        co=0
        PacketData.objects.all().delete()
        # Iterate over each packet data in the list
        for packet_data in packet_data_list:
            co+=1
            print(co)
            if co==1000:
                break
            # print(packet_data)
            # Deserialize the packet data
            new_packet_data = { 'frame_number': packet_data['frame.number'][0],
            'frame_time': packet_data['frame.time'][0],
            'frame_len': int(packet_data['frame.len'][0]) if 'frame.len' in packet_data else None,
            'eth_src': packet_data['eth.src'][0] if 'eth.src' in packet_data else None,
            'eth_dst': packet_data['eth.dst'][0] if 'eth.dst' in packet_data else None,
            'eth_type': packet_data['eth.type'][0] if 'eth.type' in packet_data else None,
            'ip_src': packet_data['ip.src'][0] if 'ip.src' in packet_data else None,
            'ip_dst': packet_data['ip.dst'][0] if 'ip.dst' in packet_data else None,
            'ip_proto': packet_data['ip.proto'][0] if 'ip.proto' in packet_data else None,
            'ip_ttl': int(packet_data['ip.ttl'][0]) if 'ip.ttl' in packet_data else None,
            'tcp_srcport': int(packet_data['tcp.srcport'][0]) if 'tcp.srcport' in packet_data else None,
            'tcp_dstport': int(packet_data['tcp.dstport'][0]) if 'tcp.dstport' in packet_data else None,
            'tcp_flags': packet_data['tcp.flags'][0] if 'tcp.flags' in packet_data else None,
            'tcp_seq': int(packet_data['tcp.seq'][0]) if 'tcp.seq' in packet_data else None,
            'udp_srcport': int(packet_data['udp.srcport'][0]) if 'udp.srcport' in packet_data else None,
            'udp_dstport': int(packet_data['udp.dstport'][0]) if 'udp.dstport' in packet_data else None,
            'udp_length': int(packet_data['udp.length'][0]) if 'udp.length' in packet_data else None,
            'http_request_method': packet_data['http.request.method'][0] if 'http.request.method' in packet_data else None,
            'http_response_code': int(packet_data['http.response.code'][0]) if 'http.response.code' in packet_data else None,
            'http_host': packet_data['http.host'][0] if 'http.host' in packet_data else None,
            'dns_qry_name': packet_data['dns.qry.name'][0] if 'dns.qry.name' in packet_data else None,
            'dns_resp_name': packet_data['dns.resp.name'][0] if 'dns.resp.name' in packet_data else None,
            'dns_flags_response': packet_data['dns.flags.response'][0] if 'dns.flags.response' in packet_data else None
            
            }
            
            
            serializer = PacketDataSerializer(data=new_packet_data)

            # If the data is valid, save it to the database
            if serializer.is_valid():
                serializer.save()
            else:
                # Handle invalid data, for example, log it or raise an exception
                raise ValidationError(serializer.errors)

        # Optionally, return something, like the number of packets saved
        print(f"Saved {len(packet_data_list)} packets")
        return 
        
            


    def post(self, request, format=None):
        try:
            # Use request.FILES for file uploads
            print("Files received in POST request:", request.FILES.keys())
            file_obj = request.FILES['pcap_file']
        except KeyError:
            # Return an error response if 'file' is not in request.FILES
            print("Files received in POST request:", request.FILES.keys())
            return JsonResponse({'error': 'No file part in the request'}, status=400)

        # Define the path within the media folder where the file will be saved
        file_path = 'pcap_files/' + file_obj.name

        # Save the file
        default_storage.save(file_path, ContentFile(file_obj.read()))
        file_path = 'media/' + file_path
        self.run_tshark(file_path, file_path.replace('.pcap', '.json'))

        print(file_path)  # Print the path where the file is saved
        json_file_path = 'media/' + 'json_files/' + file_obj.name.replace('.pcap', '.json')
        
        self.save_packet_data(json_file_path)
        print(f" yeh haina {file_path}")
        
        
        return JsonResponse({'message': 'File uploaded successfully'}, status=200)
    
    def get(self, request, format=None):
    
        return render(request, 'pcap_upload/pcap_upload.html')
