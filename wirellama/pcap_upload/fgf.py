from llama_agents import LlamaAgentsClient, AsyncLlamaAgentsClient
from time import sleep
client = LlamaAgentsClient("http://127.0.0.1:8027")  # i.e. http://127.0.0.1:8001
task_id = client.create_task("What is the number of rows in pcap_upload_packetdata table?")
print(task_id)
# <Wait a few seconds>
# returns TaskResult or None if not finished
sleep(10)
result = client.get_task_result(task_id)
print(result)