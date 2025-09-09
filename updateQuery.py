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
from SqlQueries import queryString as qStr

load_dotenv()

def update(entidade_id, query, sheetId, uBDa, uBDp, uBDs, uBDv, uBDt, uBDr):
    sql = qStr.queryString(query).format(a=entidade_id, BDa=uBDa, BDv=uBDv, BDp=uBDp, BDs=uBDs, BDt=uBDt, BDr=uBDr)
    idQuery = aws.idQuery(sql)
    aws.DownloadResultQuery(aws.getQuery(idQuery))
    arquivo_csv = open(f'DownloadsData/{idQuery}.csv', newline='', encoding='utf-8')
    leitor_csv = csv.reader(arquivo_csv)
    leitor_csv = list(leitor_csv)
    leitor_csv = leitor_csv[1:]
    query = query.upper()
    RANGE = os.getenv(query)
    fc.postSheet(sheetId, fc.credenciais(), RANGE, leitor_csv)


