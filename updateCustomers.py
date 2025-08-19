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
import updatesQueries as up 

def updateVtrp():
    up.update(76, "alertas", "VTRP_ID")
    up.update(76, "atendimentos", "VTRP_ID")
    up.update(76, "teleconsultas", "VTRP_ID")
    up.update(76, "cidades", "VTRP_ID")
    up.update(76, "fluxos", "VTRP_ID")
    up.update(76, "cid", "VTRP_ID")
    up.update(76, "comorbidades", "VTRP_ID")
    up.update(76, "idade", "VTRP_ID")
    up.update(76, "sexo", "VTRP_ID")

def updateLitoral():
     return 0 

def updateMaringa():
     return 0 