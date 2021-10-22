import json
import sys
from azure.identity import ClientSecretCredential
from azure.storage.blob import ContainerClient, BlobClient, ContentSettings
from common import file_md5, getLogger

logger = getLogger(__name__)

if len(sys.argv) != 2:
    print("USAGE) python list.py https://STORAGE_ACCOUNT.blob.core.windows.net/CONTAINER_NAME/path/to/", file=sys.stderr)
    sys.exit(1)

target_url = sys.argv[1]

with open('credentials.json') as fp:
    json_credentials = json.load(fp)

# ref: https://docs.microsoft.com/en-us/python/api/azure-identity/azure.identity.clientsecretcredential?view=azure-python
credential = ClientSecretCredential(json_credentials["tenant"], json_credentials["appId"], json_credentials["password"])

try:
    import urllib.parse
    parsed_target_url = urllib.parse.urlparse(target_url)
    logger.info(parsed_target_url)

    # /container_name/path/to/blob-prefix => "", "container_name", "path/to/blob-prefix"
    splitted_path = parsed_target_url.path.split("/", maxsplit=2)
    
    if len(splitted_path) <= 1 or splitted_path[1] == "":
        raise Exception("required container_name. eg.) https://STORAGE_ACCOUNT.blob.core.windows.net/CONTAINER_NAME")
    container_name = splitted_path[1]
    blob_name_prefix = ""
    if len(splitted_path) >= 3:
        blob_name_prefix =  splitted_path[2]
    
    container_url = f"{parsed_target_url.scheme}://{parsed_target_url.hostname}/{container_name}"

    client = ContainerClient.from_container_url(container_url, credential)
    for blob in client.list_blobs(name_starts_with=blob_name_prefix):
        logger.info(f"{blob.name}")

except Exception as e:
    logger.error("List blobs failed.", e)
