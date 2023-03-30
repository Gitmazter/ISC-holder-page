import requests
import json
import time 

API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjcmVhdGVkQXQiOjE2Nzk0MDYyOTMzNzksImVtYWlsIjoicGhpbGlwLmFuZGVsaWNAZ21haWwuY29tIiwiYWN0aW9uIjoidG9rZW4tYXBpIiwiaWF0IjoxNjc5NDA2MjkzfQ.tXTxsQtNuozzX5OCdGLfIMaqH-KdVQJjAtfKq91ReDs";
ISC_MINT_AUTHORITY = "3XM6WqYLx5gKpRNwnCcUrBmJAhRHx3imktwEvbRwXavZ"


def callHoldersApi(): 
    URL = "https://public-api.solscan.io/token/holders?tokenAddress=J9BcrQfX4p9D1bvLzRNCbMDv8f44a9LFdeqNE4Yk2WMD&limit=50&offset=0"
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

def query_mint_authority():
    mints = []
    URL = "https://public-api.solscan.io/account/transactions?account=3XM6WqYLx5gKpRNwnCcUrBmJAhRHx3imktwEvbRwXavZ&limit=50"
    headers = {"token":API_KEY}   
    res = requests.get(URL, headers=headers)
    response = json.loads(res.text) #Transactions from Mint Auth, need to scan individual TXs for Mint Proof
    for tx in response:
        txData = get_tx_data(tx['txHash'])
         
        mintTxData = check_tx_data_for_mint(txData, tx['txHash'])
        if mintTxData != None:
            # print("mintTxData:")
            # print(mintTxData) ## Returns None if no Mint
            mints.append(mintTxData)
    
    #print(mints[3])
    return mints



def get_tx_data(txHash):
    URL ="https://public-api.solscan.io/transaction/" + txHash
    headers = {"token":API_KEY}   
    res = requests.get(URL, headers=headers)
    txData = json.loads(res.text)

    return txData


def check_tx_data_for_mint(txData, txHash):
    mintTxData = {"txHash":txHash, "timeStamp":txData['blockTime'], "amountMinted":""}
    instructions = txData['parsedInstruction']

    for parsedInstruction in instructions:
        params = parsedInstruction['params']
        try:
            if params['mint']:
                mintTxData['amountMinted'] = params['tokenAmount']['amount']
                return mintTxData;  
        except:
            return None # Gracefully handling non-mint transactions from Authority
