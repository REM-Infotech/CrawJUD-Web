from flask import Flask

import os
import json
import zipfile
import requests
import openpyxl
from google.oauth2.service_account import Credentials
from google.cloud.storage import Client, Bucket
from contextlib import suppress
from requests.exceptions import ConnectionError, ConnectTimeout

from dotenv import dotenv_values

def storageClient() -> Client:
    
    project_id = dotenv_values().get("project_id")
    credentials_dict = json.loads(dotenv_values().get("credentials_dict"))

    # Configure a autenticação para a conta de serviço do GCS
    credentials = Credentials.from_service_account_info(
        credentials_dict).with_scopes(['https://www.googleapis.com/auth/cloud-platform'])

    return Client(credentials=credentials, project=project_id)
    
def bucket(storageClient: Client, bucket_name: str = None) -> Bucket:
    
    if not bucket_name:
        bucket_name = dotenv_values().get("bucket_name")
        
    bucket_obj = storageClient.bucket(bucket_name)  
    return bucket_obj


class QueueBot:
    
    def start_job(self, itens: list, app: Flask) -> int:
        
        try:
            args: dict = itens[0]
            
            args["rows"] = self.info_rows(itens[1])
            
            object_name, file_path = self.zip_arquivo(itens[2], app)
            
            args["filename"] = object_name
            
            self.upload_to_gcs(file_path, object_name)

            return self.send_signal(args)
            
        except Exception as e:
            return 500
        
    def info_rows(self, path_xlsx: str) -> str:
        
        input_filename = path_xlsx
        wrkbk_input = openpyxl.load_workbook(filename=input_filename)
        sheet_input = wrkbk_input.active
        return str(sheet_input.max_row)

    def zip_arquivo(self, identify: str, app: Flask) -> tuple[str, str]:
        
        file_paths = []
        temp_path = os.path.join(app.config['CSV_TEMP_PATH'], identify)
        for root, dirs, files in os.walk(temp_path):
            for file in files:
                
                file_path = os.path.join(app.config['CSV_TEMP_PATH'], identify, file)
                file_paths.append(file_path)
        
        namezip = f"{identify}.zip"
        
        zip_file = os.path.join(app.config['CSV_TEMP_PATH'], namezip)       
        with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file in file_paths:
                zipf.write(file)
                
        return (namezip, zip_file)

    def upload_to_gcs(self, file_path: str,  object_name: str):
        
        arquivo_local = file_path
        objeto_destino = object_name
        bucket_name = "temporary_files"

        blob = bucket(storageClient(), bucket_name).blob(objeto_destino)

        # Faz o upload do arquivo local para o objeto Blob
        blob.upload_from_filename(arquivo_local)
        
    def send_signal(self, args: dict) -> int:
        
        server = dotenv_values().get("url")
            
        status_code = 500
        with suppress(ConnectTimeout, ConnectionError):
            sinal = requests.post(url=server, data=args, timeout=30)
            status_code = sinal.status_code
            
        return status_code
    