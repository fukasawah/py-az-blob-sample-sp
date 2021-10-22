import json
import sys
from azure.identity import ClientSecretCredential
from azure.storage.blob import BlobClient
from common import file_md5, getLogger

logger = getLogger(__name__)

if len(sys.argv) != 3:
    print("USAGE) python upload.py file.txt https://STORAGE_ACCOUNT.blob.core.windows.net/CONTAINER_NAME/path/to/file.txt", file=sys.stderr)
    sys.exit(1)

download_src = sys.argv[1]
download_dest = sys.argv[2]

with open('credentials.json') as fp:
    json_credentials = json.load(fp)

# ref: https://docs.microsoft.com/en-us/python/api/azure-identity/azure.identity.clientsecretcredential?view=azure-python
credential = ClientSecretCredential(json_credentials["tenant"], json_credentials["appId"], json_credentials["password"])

blob_client = BlobClient.from_blob_url(download_src, credential=credential)

try:
    with open(download_dest, 'wb') as fp:
        # https://docs.microsoft.com/en-us/python/api/azure-storage-blob/azure.storage.blob.blobclient?view=azure-python#download-blob-offset-none--length-none----kwargs-
        downloader = blob_client.download_blob() 
        downloader.download_to_stream(fp)
        download_md5 = downloader.properties["content_settings"]["content_md5"]
        
    # done download. check md5
    local_md5 = file_md5(download_dest).digest()

    # # error test flip bit
    # local_md5 = bytearray(local_md5)
    # local_md5[0] ^= 0x01 

    if  local_md5 != download_md5:
        raise Exception(f"file was broken. local_md5={local_md5}, download_md5={download_md5}")
    
    # Successed
    logger.info(f"{downloader.properties}")
    
except Exception as e:
    logger.error("Download failed.", e)
