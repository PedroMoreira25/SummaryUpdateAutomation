import os 
import pandas as pd 
import functions as fc

from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
load_dotenv()
SAMPLE_SPREADSHEET_ID = os.getenv("SAMPLE_SPREADSHEET_ID")
SAMPLE_RANGE_NAME = os.getenv("SAMPLE_RANGE_NAME")

creds = fc.credenciais()

fc.getSheet(SAMPLE_SPREADSHEET_ID, creds, SAMPLE_RANGE_NAME)

fc.postSheet(SAMPLE_SPREADSHEET_ID, creds, SAMPLE_RANGE_NAME)

fc.getSheet(SAMPLE_SPREADSHEET_ID, creds, SAMPLE_RANGE_NAME)
