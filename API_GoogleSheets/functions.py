
import os 
import pandas as pd 
from pprint import pprint 
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
load_dotenv()
SAMPLE_SPREADSHEET_ID = os.getenv("SAMPLE_SPREADSHEET_ID")
SAMPLE_RANGE_NAME = os.getenv("SAMPLE_RANGE_NAME")
print(SAMPLE_SPREADSHEET_ID+"\n")
# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

def credenciais(): 

    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json", SCOPES
        )
            creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())
    return creds



def getSheet(sheetId, creds2, range):
    try:
        service = build("sheets", "v4", credentials=creds2)

    # Call the Sheets API
        sheet = service.spreadsheets()

    # LER informações do Google Sheets
        result = (
            sheet.values()
            .get(spreadsheetId=sheetId, range=range)
            .execute()
        )
    
        dados = (result['values'])
        return dados 

    except HttpError as err:
        print(err)


def getIndexLastRowSheet(sheetId, cred, range): #traz o índice da última linha com dados preenchidos da planilha
    try: 
        service = build("sheets", "v4", credentials=cred)

    # Call the Sheets API
        sheet = service.spreadsheets()

    # LER informações do Google Sheets
        result = (
            sheet.values()
            .get(spreadsheetId=sheetId, range=range)
            .execute()
        )
    
        dados = (result['values'])
        IndexLastRow = (len(dados))
        return IndexLastRow

    except HttpError as err:
        print(err)

    

# O postSheet abaixo faz um post na planilha usando o método append
def postSheet(sheetId, creds1, range1, dados):
    try:
        service = build("sheets", "v4", credentials=creds1)
        #Call the sheets API
        sheet = service.spreadsheets()
        result = (sheet.values().append(spreadsheetId=sheetId,
                                                    range=range1, valueInputOption="USER_ENTERED", body={'values': dados}).execute())
        return result
    except HttpError as err:
        print(err)


# o postSheet abaixo faz um post de dados na planilha usando o método update
"""
def postSheet(sheetId, cred, range, dados):
    try: 
        service = build("sheets", "v4", credentials=cred)
        #Call the sheets API
        sheet = service.spreadsheets()
        result = sheet.values().update(spreadsheetId=sheetId,
                                       range=range, valueInputOption="USER_ENTERED", body = {'values': dados}).execute()
        return result
    except HttpError as err:
        print(err)
"""
# o postSheet abaixo faz um post de dados na planilha usando o método batchUpdate
"""
def postSheet(sheetId, cred, range, dados):
    try:
        service = build("sheets", "v4", credentials=cred)
        #Call the sheets API
        sheet = service.spreadsheets()
        data = [
            {"range": range, "values": dados}
        ]
        body = {"valueInputOption": "USER_ENTERED", "data": data}
        result = sheet.values().batchUpdate(spreadsheetId=sheetId, body=body).execute()
        return result
    except HttpError as err:
        print(err)
"""