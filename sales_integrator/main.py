from google.cloud import storage
from google.cloud import bigquery
from google.cloud.bigquery import SchemaField
from google.api_core.exceptions import Conflict
from datetime import date
import datetime
from pytz import timezone
import time
import json

# Efetua a importação do módulo json e abrir o arquivo config.json
with open('config.json', 'r')  as f:
    config_data = json.load(f)

table_name_log = config_data["BIGQUERY"]["table_name_log"]
project_id = config_data["BIGQUERY"]["project_id"]
dataset_id = config_data["BIGQUERY"]["dataset_id"]

def read_gcs(event, context):
    """Triggered by a change to a Cloud Storage bucket.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    
    bucket_name = event['bucket']
    file_name = event['name']
    if "sales_integrator" in file_name:
        try:
    
            storage_client = storage.Client()
            bucket = storage_client.get_bucket(bucket_name)
            blob = bucket.blob(file_name)
            file_content = blob.download_as_text()
    
            while not table_exists(project_id, dataset_id):
                create_table(project_id, dataset_id)

            insert_data(file_content, file_name, project_id, dataset_id)
        
        except Exception as e:
            current_timestamp = datetime.datetime.now(timezone('America/Sao_Paulo')).strftime("%Y-%m-%d %H:%M:%S")
            insert_error_log(str(e), file_name, current_timestamp, project_id, dataset_id, table_name_log)
            raise

def insert_error_log(errors, file_name, current_timestamp, project_id, dataset_id, table_name_log):
    bigquery_client = bigquery.Client()
    table_ref_log = f"{project_id}.{dataset_id}.{table_name_log}"
    rows_log = [{"payload": str(errors), "timestamp_ingestion": current_timestamp, "uri": file_name}]
    log = bigquery_client.insert_rows_json(table_ref_log, rows_log)


def insert_data(file_content, file_name, project_id, dataset_id):
    current_date = datetime.datetime.now(timezone('America/Sao_Paulo')).strftime("%Y%m%d")
    table_name = config_data["BIGQUERY"]["table_name"] 
    bigquery_client = bigquery.Client()
    table_ref = f"{project_id}.{dataset_id}.{table_name}{current_date}"

    current_timestamp = datetime.datetime.now(timezone('America/Sao_Paulo')).strftime("%Y-%m-%d %H:%M:%S")
    rows = [{"payload": file_content, "timestamp_ingestion": current_timestamp, "uri": file_name}]
    
    max_attempts = 3  # Define o número máximo de tentativas
    attempts = 0  # Contador de tentativas
    error_messages = set()  

    while attempts < max_attempts:
        attempts += 1
        
        try:
            errors = bigquery_client.insert_rows_json(table_ref, rows)
    
            if errors == []:
                print("Dados inseridos com sucesso.")
                return  
            
        except Exception as e:
            if "404 POST" in str(e):
                error_messages.add(str(e)) 
            else:
                error_messages.add(str(e)) 
                raise
                
    # Se todas as tentativas falharem, efetua a escrita na tabela de log.
    error_messages_str = "\n".join(error_messages)  
    insert_error_log(error_messages_str, file_name, current_timestamp, project_id, dataset_id, table_name_log)

def create_table(project_id, dataset_id):
    current_date = datetime.datetime.now(timezone('America/Sao_Paulo')).strftime("%Y%m%d")
    table_name = config_data["BIGQUERY"]["table_name"] 
    client = bigquery.Client()

    # Definindo o schema da tabela.
    schema = [
        SchemaField("payload", "STRING"),
        SchemaField("timestamp_ingestion", "TIMESTAMP"),
        SchemaField("uri", "STRING"),

    ]

    table_config = bigquery.Table(f"{project_id}.{dataset_id}.{table_name}{current_date}", schema=schema)
    table_config.time_partitioning = bigquery.TimePartitioning(
    type_=bigquery.TimePartitioningType.HOUR
)

    # Definindo as opções de clusterização
    table_config.clustering_fields = ["timestamp_ingestion"]

    try:
        table = client.create_table(table_config)
        print(f"Tabela criada {table_name}{current_date} com sucesso.")
    except Conflict:
       
        print("Tabela já existente.")

def table_exists(project_id, dataset_id):
    current_date = datetime.datetime.now(timezone('America/Sao_Paulo')).strftime("%Y%m%d")
    table_name = config_data["BIGQUERY"]["table_name"] 
    client = bigquery.Client()
    table_ref = f"{project_id}.{dataset_id}.{table_name}{current_date}"
    try:
        client.get_table(table_ref)
        return True
    except Exception as e:
        if "Not found" in str(e):
            return False
        else:
            raise
     


