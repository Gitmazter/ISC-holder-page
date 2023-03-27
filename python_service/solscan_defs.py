import requests
import json
import time 
import csv

API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjcmVhdGVkQXQiOjE2Nzk0MDYyOTMzNzksImVtYWlsIjoicGhpbGlwLmFuZGVsaWNAZ21haWwuY29tIiwiYWN0aW9uIjoidG9rZW4tYXBpIiwiaWF0IjoxNjc5NDA2MjkzfQ.tXTxsQtNuozzX5OCdGLfIMaqH-KdVQJjAtfKq91ReDs";

def callHoldersApi(): 
    URL = "https://public-api.solscan.io/token/holders?tokenAddress=J9BcrQfX4p9D1bvLzRNCbMDv8f44a9LFdeqNE4Yk2WMD&limit=29&offset=0"
    headers = {"token":API_KEY}
    res = requests.get(URL, headers=headers)
    response = json.loads(res.text)
    return response

def callMetaApi():
    URL = "https://public-api.solscan.io/token/meta?tokenAddress=J9BcrQfX4p9D1bvLzRNCbMDv8f44a9LFdeqNE4Yk2WMD"
    headers = {"token":API_KEY}
    res = requests.get(URL, headers=headers)
    response = json.loads(res.text)
    return response

def getUserTxData(address):
    prevTime = "0";
    timeNow = str(round(time.time()))

    URL = "https://public-api.solscan.io/account/exportTransactions?account="+ address + "&type=tokenchange&fromTime=" + prevTime + "&toTime=" + timeNow;
    headers = {"accept":"application/json", "token":API_KEY}
    res = requests.get(URL, headers=headers)

    resCsvStr = res.text

    return resCsvStr #This is the CSV data for an Accounts Token Txs
