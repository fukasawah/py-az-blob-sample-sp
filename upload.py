import json
import sys
from azure.identity import ClientSecretCredential
from azure.storage.blob import BlobClient, ContentSettings
from common import file_md5, getLogger

logger = getLogger(__name__)

if len(sys.argv) != 3:
    print("USAGE) python upload.py file.txt https://STORAGE_ACCOUNT.blob.core.windows.net/CONTAINER_NAME/path/to/file.txt", file=sys.stderr)
    sys.exit(1)

upload_src = sys.argv[1]
upload_dest = sys.argv[2]

with open('credentials.json') as fp:
    json_credentials = json.load(fp)

# ref: https://docs.microsoft.com/en-us/python/api/azure-identity/azure.identity.clientsecretcredential?view=azure-python
credential = ClientSecretCredential(json_credentials["tenant"], json_credentials["appId"], json_credentials["password"])

blob_client = BlobClient.from_blob_url(upload_dest, credential=credential)

# ref: https://docs.microsoft.com/en-us/python/api/azure-storage-blob/azure.storage.blob.blobclient?view=azure-python#upload-blob-data--blob-type--blobtype-blockblob---blockblob----length-none--metadata-none----kwargs-

try:
    with open(upload_src, 'rb') as fp:
        res = blob_client.upload_blob(fp, validate_content=True, overwrite=True) 

    # Successed
    logger.info(res)
except Exception as e:
    logger.error("Upload failed.", e)
