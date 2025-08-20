import boto3 
import time 
import os 
import pandas as pd 
from pprint import pprint
from dotenv import load_dotenv

load_dotenv()
ACCESS_KEY=os.getenv("AWS_ACCESS_KEY_ID")
SECRET_KEY=os.getenv("AWS_SECRET_ACCESS_KEY")

SESSION_TOKEN=os.getenv("AWS_SESSION_TOKEN")



session = boto3.Session(
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    aws_session_token=SESSION_TOKEN,
    region_name='us-east-1'
)



def idQuery(query: str): #aqui realizamos a query no Athena e obtemos o id dela
    idDaQuery = session.client('athena').start_query_execution(
        QueryString=query,
        QueryExecutionContext={'Database':'product' },
        ResultConfiguration={'OutputLocation':'s3://output.athena/' }
    )
    print(idDaQuery['QueryExecutionId'])
    return idDaQuery['QueryExecutionId']


def getQuery(idQuery1): #aqui esperamos a query ser executada
    key = False 
    while key == False:
        resposta = session.client('athena').get_query_execution(QueryExecutionId=idQuery1)
        status = resposta['QueryExecution']['Status']['State']
        if status in {'SUCCEEDED', 'FAILED', 'CANCELLED'}:
            return resposta['QueryExecution']['QueryExecutionId']
            key = True
            break
        time.sleep(1)
        print("Executando a query...") #programa dorme por um segundo

def DownloadResultQuery(idQuery):
    s3 = boto3.client('s3')
    s3.download_file('output.athena', f'{idQuery}.csv', f'DownloadsData/{idQuery}.csv')
    