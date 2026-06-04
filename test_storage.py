from azure.storage.blob import BlobServiceClient
import os
from dotenv import load_dotenv

load_dotenv()

conn = os.getenv("AZURE_STORAGE_CONNECTION_STRING")

client = BlobServiceClient.from_connection_string(conn)

print("Connected")

for c in client.list_containers():
    print(c.name)