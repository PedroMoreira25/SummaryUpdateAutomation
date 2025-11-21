import boto3 
import time 
import os 
from pprint import pprint
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from API_GoogleSheets import functions as fc
from updateQuery import update 
import idCustomer as idc 

load_dotenv()

BDp = os.getenv("BDpessoas")
BDa = os.getenv("BDalertas")
BDv = os.getenv("BDrespostas")
BDs = os.getenv("BDcid")
BDt = os.getenv("BDfalar")
BDr = os.getenv("BDrecord")
BDs2 = os.getenv("BDcid2")

LIT_EID = os.getenv("LIT_EID")
VTRP_EID = os.getenv("VTRP_EID")
SALTO_EID = os.getenv("SALTO_EID")
SUL_EID = os.getenv("SUL_EID")
NORO_EID = os.getenv("NORO_EID")
MAR_EID = os.getenv("MAR_EID")

LITORAL_ID = os.getenv("LITORAL_ID")
VTRP_ID = os.getenv("VTRP_ID")
SALTOSPREADSHEET_ID = os.getenv("SALTO_SPREADSHEET_ID")
SULCAPIXABA_SPREADSHEET_ID = os.getenv("SULCAPIXABA_SPREADSHEET_ID")
NOROESTECAPIXABA_SPREADSHEET_ID = os.getenv("NOROESTECAPIXABA_SPREADSHEET_ID")
MARINGA_SPREADSHEET_ID = os.getenv("MARINGA_SPREADSHEET_ID")

eid = [LIT_EID, SALTO_EID, SUL_EID, NORO_EID, MAR_EID]
query = ["alertas", "atendimentos", "cid", "cidades", "comorbidades", "fluxos", "idade", "sexo", "teleconsultas"]
idp = [LITORAL_ID, SALTOSPREADSHEET_ID, SULCAPIXABA_SPREADSHEET_ID, NOROESTECAPIXABA_SPREADSHEET_ID, MARINGA_SPREADSHEET_ID]

""" a = 0 
for entidade_id in eid:
    idPlanilha = idp[a]
    for qry in query: 
        print(idc.idCustomer(int(entidade_id)))
        print(qry)
        update(entidade_id, qry, idPlanilha, BDa, BDp, BDs, BDv, BDt, BDr)
    a = a + 1 
    print()
    print()
 """
a = 0
for entidade_id in eid:
    idPlanilha = idp[a]
    query = idc.queriesCustomer(int(entidade_id))
    for qry in query:
        print(idc.idCustomer(int(entidade_id)))
        print(qry)
        update(entidade_id, qry, idPlanilha, BDa, BDp, BDs, BDv, BDt, BDr, BDs2)
    a = a + 1 
    print()
    print()