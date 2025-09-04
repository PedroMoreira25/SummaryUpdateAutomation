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

HUGV_EID=os.getenv("HUGV_EID")
HMD_EID=os.getenv("HMD_EID")
HUSC_EID=os.getenv("HUSC_EID")
HCPF_EID=os.getenv("HCPF_EID")
HMRG_EID=os.getenv("HMRG_EID")

HCPF_IDP=os.getenv("HCPF_IDP")
HMD_IDP=os.getenv("HMD_IDP")
HUSC_IDP=os.getenv("HUSC_IDP")
HUGV_IDP=os.getenv("HUGV_IDP")
HMRG_IDP=os.getenv("HMRG_IDP")

tt = " gt"
uu = " utyj"
vv = "bgv"
ww = "efr"
xx = "!refe"
yy = "35rre3"

eid = [HCPF_EID, HUSC_EID, HUGV_EID, HMRG_EID]
query = "fluxos"
idp = [HCPF_IDP, HUSC_IDP, HUGV_IDP, HMRG_IDP]

a = 0 
for entidade_id in eid:
    idPlanilha = idp[a] 
    print(query) 
    update(entidade_id, query, idPlanilha, tt, uu, vv, ww, xx, yy)
    a = a + 1 
    print()
    print()

