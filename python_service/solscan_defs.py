import requests
import json
import time 
from settings import GET_KEY

ISC_MINT_AUTHORITY = "3XM6WqYLx5gKpRNwnCcUrBmJAhRHx3imktwEvbRwXavZ" 
headers = {"token":str(GET_KEY("SOLSCAN_API_KEY"))}  

def callHoldersApi(offset): 
    URI = "https://public-api.solscan.io/token/holders?tokenAddress=J9BcrQfX4p9D1bvLzRNCbMDv8f44a9LFdeqNE4Yk2WMD&limit=50&offset=" + str(offset)
    res = requests.get(URI, headers=headers)
    response = json.loads(res.text)
    return response

def callMetaApi():
    URI = "https://public-api.solscan.io/token/meta?tokenAddress=J9BcrQfX4p9D1bvLzRNCbMDv8f44a9LFdeqNE4Yk2WMD"
    res = requests.get(URI, headers=headers)
    response = json.loads(res.text)
    return response

def getUserTxData(address):
    prevTime = "0";
    timeNow = str(round(time.time()))
    URI = "https://public-api.solscan.io/account/exportTransactions?account="+ address + "&type=tokenchange&fromTime=" + prevTime + "&toTime=" + timeNow;
    res = requests.get(URI, headers=headers)

    resCsvStr = res.text

    return resCsvStr #This is the CSV data for an Accounts Token Txs

def getAllTxs(offset):
    ## Get all txs with offset 



def query_mint_authority():
    mints = []
    URI = "https://public-api.solscan.io/account/transactions?account=3XM6WqYLx5gKpRNwnCcUrBmJAhRHx3imktwEvbRwXavZ&limit=50"  
    res = requests.get(URI, headers=headers)
    response = json.loads(res.text) #Transactions from Mint Auth, need to scan individual TXs for Mint Proof
    for tx in response:
        txData = get_tx_data(tx['txHash'])
         
        mintTxData = check_tx_data_for_mint(txData, tx['txHash'])
        if mintTxData != None:
            mints.append(mintTxData)
    
    return mints

def get_tx_data(txHash):
    URI ="https://public-api.solscan.io/transaction/" + txHash
    res = requests.get(URI, headers=headers)
    txData = json.loads(res.text)
    return txData


def check_tx_data_for_mint(txData, txHash):
    mint_post = {"_id":txHash, "timeStamp":txData['blockTime'], "amountMinted":""}
    instructions = txData['parsedInstruction']

    for parsedInstruction in instructions:
        params = parsedInstruction['params']
        try:
            if params['mint']:
                mint_post['amountMinted'] = params['tokenAmount']['amount']
                return mint_post;  
        except:
            return None # Gracefully handling non-mint transactions from Authority
