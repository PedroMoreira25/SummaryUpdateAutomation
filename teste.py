from API_GoogleSheets import functions as fc 
import csv
import time
import os 
from AWS import AWS as aws 
import boto3
from SqlQueries import queryString as qStr

alert = os.getenv("BDalertas") 
pessoas = os.getenv("BDpessoas")
cid = os.getenv("BDcid")
vital = os.getenv("BDrespostas")
team = os.getenv("BDfalar")
record = os.getenv("BDrecord")

LIT_EID = os.getenv("LIT_EID")

tBd = [alert, pessoas, cid, vital, team, record]

def showQuery(entidade_id, query, uBDa, uBDp, uBDs, uBDv, uBDt, uBDr):
    sql = qStr.queryString(query).format(a=entidade_id, BDa=uBDa, BDv=uBDv, BDp=uBDp, BDs=uBDs, BDt=uBDt, BDr=uBDr)
    print(sql)
    print("\n") 
    print("\n") 
    print("---------------------------------------------------------------------------------------------")
    print("\n") 
    print("\n") 

queries = ["alertas", "atendimentos", "cid", "cidades", "comorbidades", "fluxos", "idade", "sexo", "teleconsultas"]

for q in queries:
    showQuery(LIT_EID, q, alert, pessoas, cid, vital, team, record)


    