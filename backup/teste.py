import boto3
import pandas as pd
import time
import os 
from dotenv import load_dotenv

# Configurações
DATABASE = 'product'
QUERY = """
SELECT DISTINCT atendimento_id, resultado, DATE(data_alerta)
    FROM lc_alert 
        WHERE 
            entidade_id=76 
        LIMIT 5;

"""
S3_OUTPUT = 's3://output.athena/'
LOCAL_FILE = 'dados/testesave.csv'

load_dotenv()
ACCESS_KEY=os.getenv("AWS_ACCESS_KEY_ID")
SECRET_KEY=os.getenv("AWS_SECRET_ACCESS_KEY")
SESSION_TOKEN=os.getenv("AWS_SESSION_TOKEN")

# Sessão com credenciais temporárias
session = boto3.Session (
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    aws_session_token=SESSION_TOKEN,
    region_name='us-east-1'
)

athena = session.client('athena') #meio que liga o Athena
s3 = session.client('s3')         #meio que liga o S3

def run_athena_query(query, database, s3_output):
    response = athena.start_query_execution(
        QueryString=query,
        QueryExecutionContext={'Database': database},
        ResultConfiguration={'OutputLocation': s3_output}
    )
    return response['QueryExecutionId']

def wait_for_query(query_execution_id):
    while True:
        result = athena.get_query_execution(QueryExecutionId=query_execution_id)
        status = result['QueryExecution']['Status']['State']
        if status in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
            return status
        time.sleep(2)

def download_results(query_execution_id):
    print("Baixando arquivo de resultados do S3...")
    bucket = S3_OUTPUT.replace("s3://", "").split("/")[0]
    prefix = "/".join(S3_OUTPUT.replace("s3://", "").split("/")[1:])
    s3_key = f"{prefix}{query_execution_id}.csv" if prefix else f"{query_execution_id}.csv"
    s3.download_file(bucket, s3_key, LOCAL_FILE)
    print(f"Arquivo salvo localmente como: {LOCAL_FILE}")

def main():
    print("Executando query no Athena...")
    query_id = run_athena_query(QUERY, DATABASE, S3_OUTPUT)

    print("Aguardando execução da query...")
    status = wait_for_query(query_id)

    if status != 'SUCCEEDED':
        print(f"Erro: query terminou com status '{status}'")
        return

    download_results(query_id)

    print("Abrindo resultado com pandas:")
    df = pd.read_csv(LOCAL_FILE)
    print(df.head())
    print(len(df.index))

if __name__ == "__main__":
    main()