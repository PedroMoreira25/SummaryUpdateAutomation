
import os 
import pandas as pd 

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
    print(creds)
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
    
        dados = pd.DataFrame(result['values'])
        print(dados)

    except HttpError as err:
        print(err)


"""
def postSheet(sheetId, creds1, range1):
    try:
        service = build("sheets", "v4", credentials=creds1)
        # Call the Sheets API
        sheet = service.spreadsheets()
        print("\n")
        cpf = input("Digite o CPF do paciente: ")
        cor_alerta = input("Digite a cor do alerta: ")
        data = input("Digite a data do alerta em dd/mm/aaaa: ")
        inputValues = [
            [cpf, cor_alerta, data],
            ["Teste1", "TEste1", "Teste1"],
            ["Teste2", "Teste2", "Teste2"],
            ["Teste3", "Teste3", "TEste3"]
        ]
        result = (sheet.values().append(spreadsheetId=sheetId,
                                                    range=range1, valueInputOption="USER_ENTERED", body={'values': inputValues}).execute())
        return result
    except HttpError as err:
        print(err)
"""

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