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
from updatesQueries import update 

update(76, "teste", "VTRP_ID")
