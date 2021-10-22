

Usage
-----------------------

Windows + Git Bash(Git for Windows)

### Setup

```
# Create venv
python -m venv venv

# Activate Venv
. venv/Scripts/activate

# Install packages
pip install -r requirements.txt

# Create credentials.json file (service principal json)
cat << '__EOF__' >> credentials.json
{
  "appId": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "displayName": "xxxxxxxxxxxxxxx",
  "name": "http://xxxxxxxxxxxxxxx",
  "password": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "tenant": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
}
__EOF__
```

### Run sample code

```
python list.py "https://STORAGE_ACCOUNT.blob.core.windows.net/CONTAINER_NAME/path/to/file.txt"
python upload.py "file.txt" "https://STORAGE_ACCOUNT.blob.core.windows.net/CONTAINER_NAME/path/to/file.txt"
python download.py "https://STORAGE_ACCOUNT.blob.core.windows.net/CONTAINER_NAME/path/to/file.txt" "file.txt"
```


Upload Checksum survey
------------------------

### ContentSettings: Included x-ms-blob-content-md5 header

```
        md5 = hashlib.md5(data).digest()
        md5 = bytearray(md5)
        # md5[0] = 0 # emulate bit flip error
        res = blob_client.upload_blob(fp, validate_content=False, overwrite=True, content_settings=ContentSettings(content_md5=md5)) 
```

``` log
2021-10-22 15:30:33,216 [INFO] Request URL: 'https://XXXX.blob.core.windows.net/example/requirements.txt'/nRequest method: 'PUT'/nRequest headers:/n    'x-ms-blob-type': 'REDACTED'/n    'Content-Length': '34'/n    'x-ms-blob-content-md5': 'REDACTED'/n    'x-ms-version': 'REDACTED'/n    'Content-Type': 'application/octet-stream'/n    'Accept': 'application/xml'/n   
 'User-Agent': 'azsdk-python-storage-blob/12.9.0 Python/3.7.9 (Windows-10-10.0.19041-SP0)'/n    'x-ms-date': 'REDACTED'/n    'x-ms-client-request-id': '8f0262fe-3301-11ec-914d-5efa1ed3ecbb'/n    'Authorization': 'REDACTED'/nA body is sent with the request
```

### validate_content=True: Included Content-MD5 header

```
        res = blob_client.upload_blob(fp, validate_content=True, overwrite=True)
```

``` log
2021-10-22 15:06:16,154 [INFO] Request URL: 'https://XXXX.blob.core.windows.net/example/requirements.txt'/nRequest method: 'PUT'/nRequest headers:/n    'x-ms-blob-type': 'REDACTED'/n    'Content-Length': '34'/n    'x-ms-version': 'REDACTED'/n    'Content-Type': 'application/octet-stream'/n    'Accept': 'application/xml'/n    'User-Agent': 'azsdk-python-storage-blob/12.9.0 Python/3.7.9 (Windows-10-10.0.19041-SP0)'/n    'Content-MD5': 'REDACTED'/n    'x-ms-date': 'REDACTED'/n    'x-ms-client-request-id': '2a939354-32fe-11ec-bbbd-5efa1ed3ecbb'/n    'Authorization': 'REDACTED'/nA body is sent with the request
```

### validate_content=False: Not included Content-MD5 header

```
        res = blob_client.upload_blob(fp, validate_content=False, overwrite=True)
```


``` log
2021-10-22 15:08:41,586 [INFO] Request URL: 'https://XXXX.blob.core.windows.net/example/requirements.txt'/nRequest method: 'PUT'/nRequest headers:/n    'x-ms-blob-type': 'REDACTED'/n    'Content-Length': '34'/n    'x-ms-version': 'REDACTED'/n    'Content-Type': 'application/octet-stream'/n    'Accept': 'application/xml'/n    'User-Agent': 'azsdk-python-storage-blob/12.9.0 Python/3.7.9 (Windows-10-10.0.19041-SP0)'/n    'x-ms-date': 'REDACTED'/n    'x-ms-client-request-id': '8135d14a-32fe-11ec-8397-5efa1ed3ecbb'/n    'Authorization': 'REDACTED'/nA body is sent with the request
```