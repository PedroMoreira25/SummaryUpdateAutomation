import boto3 
import time 
import os 
import pandas as pd 
from pprint import pprint
from dotenv import load_dotenv

load_dotenv()
ACCESS_KEY=os.getenv("AWS_ACCESS_KEY_ID")
SECRET_KEY=os.getenv("AWS_SECRET_ACCESS_KEY")
SESSION_TOKEN=os.getenv("AWS_SESSION_TOKEN")

session = boto3.Session(
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    aws_session_token=SESSION_TOKEN,
    region_name='us-east-1'
)

s3 = boto3.client('s3')
#s3://output.athena/f1144be1-ebf6-4555-b40a-d42d6d28fe2a.csv
s3.download_file('output.athena', 'f1144be1-ebf6-4555-b40a-d42d6d28fe2a.csv', 'f1144be1-ebf6-4555-b40a-d42d6d28fe2a.csv')
