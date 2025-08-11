import boto3 
import time 
import os 
from pprint import pprint
from dotenv import load_dotenv
from AWS.AWS import exeQuery, getQuery, idQuery
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from API_GoogleSheets import functions as fc
from SqlQueries import vtrp_query as vtrp

load_dotenv()
SPREADSHEET_ID = os.getenv("VTRP_SPREADSHEET_ID") 

resultQuery = exeQuery('24f98c33-ae19-4f09-9601-f9ca82cf4451')

start = 0
end = 0 
var = 1
while start < len(resultQuery):
    RANGE = f"NEW_atendimentos!A{var}"
    end = end + 100
    fc.postSheet(SPREADSHEET_ID, fc.credenciais(), RANGE, resultQuery[start:end])
    var = var + 100
    start = end 
    print("\n")

#TEREI QUE MUDAR O postSheet !!!!!!!!!!

#fc.postSheet(SPREADSHEET_ID, fc.credenciais(), RANGE, resultQuery)
#comentarei a linha de baixo pq estou testando o programa. Porém, quando ele estiver rodando, é só descomentar a linha de baixo
#resultQuery = exeQuery(getQuery(idQuery(vtrp.atendimentos)))
# fc.getSheet(SPREADSHEET_ID, fc.credenciais(), RANGE)



"""
b = 0 
inputData = []
while a <= len(resultQuery):
    a = a + 500 
    while b < len(resultQuery):
            inputData.append(resultQuery[b])
            b = b + 1 
    fc.postSheet(SPREADSHEET_ID, fc.credenciais(), RANGE, inputData)    
"""