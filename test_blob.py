from azure.storage.blob import BlobServiceClient
import os
from dotenv import load_dotenv

load_dotenv()

conn = os.getenv("AZURE_STORAGE_CONNECTION_STRING")

client = BlobServiceClient.from_connection_string(conn)

blob = client.get_blob_client(
    container="hmsmedicalrecords",
    blob="local-test.txt"
)

blob.upload_blob(b"hello", overwrite=True)

print("UPLOAD SUCCESS")