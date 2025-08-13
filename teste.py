import boto3 
import time 
import os 
from pprint import pprint 
from dotenv import load_dotenv 
from AWS import AWS as aws 
from google.auth.transport.requests import Request 
from google.oauth2.credentials import Credentials 
from google_auth_oauthlib.flow import InstalledAppFlow 
from googleapiclient.discovery import build 
from googleapiclient.errors import HttpError 
from API_GoogleSheets import functions as fc 
from SqlQueries import vtrp_query as vtrp 

load_dotenv()

SHEETID = '130rckjo8_3mP-xx7Hg_poDn1Wsiz8RT9RH_1pXcyL-0'
#SHEETID = os.getenv("SAMPLE_SPREADSHEET_ID")
RANGE = "Página1!A:H"
#RANGE = os.getenv("SAMPLE_RANGE_NAME")
ACCESS_KEY=os.getenv("AWS_ACCESS_KEY_ID")
SECRET_KEY=os.getenv("AWS_SECRET_ACCESS_KEY")
SESSION_TOKEN=os.getenv("AWS_SESSION_TOKEN")

resultQuery = aws.exeQuery('f1144be1-ebf6-4555-b40a-d42d6d28fe2a')

print(len(resultQuery))

#def dividir_lista(listaMaior, tamanho):
#    """Divide listaMaior em sublistas de no máximo 'tamanho' elementos."""
#    return [listaMaior[i:i + tamanho] for i in range(0, len(listaMaior), tamanho)]

#def enviar_em_chunks(sheetId, creds1, range1, listaMaior, tamanho=100, delay=1):
#    """
   # Envia dados para o Google Sheets em blocos de até 'tamanho' linhas.
  #  delay = segundos entre cada envio para evitar limite de quota da API.
 #   """
#    listas_menores = dividir_lista(listaMaior, tamanho)
    
#    for i, sublista in enumerate(listas_menores):
#        print(f"Enviando chunk {i+1}/{len(listas_menores)} com {len(sublista)} linhas...")
#        fc.postSheet(sheetId, creds1, range1, sublista)
#        time.sleep(delay)  # aguarda antes do próximo envio

#dividir_lista(resultQuery, 100)
#enviar_em_chunks(SHEETID, fc.credenciais(), RANGE, resultQuery, tamanho=100, delay=1)



#lista[0] = resultQuery[0]
#lista[0] = resultQuery[1]
#lista[0] = resultQuery[2]
#lista[0] = resultQuery[...]
#lista[0] = resultQuery[99]
#lista[1] = resultQuery[100]
#lista[1] = resultQuery[101]
#lista[1] = resultQuery[102]






#fc.postSheet(SHEETID, fc.credenciais(), RANGE, resultQuery)
#