import boto3 
import time 
import os 
import pandas as pd
import csv
from pprint import pprint 
from dotenv import load_dotenv 
from AWS import AWS as aws 
from google.auth.transport.requests import Request 
from google.oauth2.credentials import Credentials 
from google_auth_oauthlib.flow import InstalledAppFlow 
from googleapiclient.discovery import build 
from googleapiclient.errors import HttpError 
from API_GoogleSheets import functions as fc 
from SqlQueries import queries as q  

load_dotenv()

def update(entidade_id: int, query: str, sheetId: str):
    sql = q.queries[query].format(a=entidade_id)
    idQuery = aws.idQuery(sql)
    aws.DownloadResultQuery(aws.getQuery(idQuery))
    arquivo_csv = open(f'DownloadsData/{idQuery}.csv')
    leitor_csv = csv.reader(arquivo_csv)
    leitor_csv = list(leitor_csv)
    query = query.upper()
    RANGE = os.getenv(query)
    SHEET_ID = os.getenv(sheetId)
    fc.postSheet(SHEET_ID, fc.credenciais(), RANGE, leitor_csv)
