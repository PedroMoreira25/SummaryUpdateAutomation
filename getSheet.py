import boto3 
import time 
import os 
import pandas as pd
from pprint import pprint
from dotenv import load_dotenv
from AWS import AWS as aws
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from API_GoogleSheets import functions as fc

RANGE = 'Página1!A:C'

dados = fc.getSheet('130rckjo8_3mP-xx7Hg_poDn1Wsiz8RT9RH_1pXcyL-0',fc.credenciais(), RANGE)
pprint(dados)
print("------------------------------------------------------" + "\n\n")

IdxLastRow = fc.getIndexLastRowSheet('130rckjo8_3mP-xx7Hg_poDn1Wsiz8RT9RH_1pXcyL-0', fc.credenciais(), RANGE)
print(IdxLastRow)

"""
try:
    service = build("sheets", "v4", credentials=fc.credenciais())
    range_names = [
        'Página1!A:C'
    ]
    result = (
        service.spreadsheets()
        .values()
        .batchGet(spreadsheetId='130rckjo8_3mP-xx7Hg_poDn1Wsiz8RT9RH_1pXcyL-0', ranges=range_names)
        .execute()
    )
    #pprint(result)
    #print("\n\n")
    
    dados = result['valueRanges'][0]['values']
    pprint(dados)
    print('\n\n')
    print(len(dados))
        

except HttpError as error:
    print(f"An error occurred: {error}")
"""



"""
'77294271-9bb2-445b-be36-4d1ca503a67d'

pprint(fc.getSheet('130rckjo8_3mP-xx7Hg_poDn1Wsiz8RT9RH_1pXcyL-0',fc.credenciais(),'Página1!A1'))
"""
