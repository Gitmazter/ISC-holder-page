import requests
import json
from services.settings import GET_KEY
from urllib.request import Request, urlopen

tokenAddress = GET_KEY("TOKEN_ADDRESS")
mintAuthority = GET_KEY("MINT_AUTHORITY")
apiKey = GET_KEY("SOLSCAN_API_KEY")

headers = {
    "token": apiKey,
    'User-Agent': 'Mozilla/5.0'
    }  

def callHoldersApi(offset): 
    URI ="https://public-api.solscan.io/token/holders?tokenAddress=" + tokenAddress + "&limit=50&offset=" + str(offset)
    req = Request(
        url=URI, 
        headers=headers
    )
    webpage = urlopen(req).read()
    response = json.loads(webpage)
    return response

def callMetaApi():
    URI = "https://public-api.solscan.io/token/meta?tokenAddress=" + tokenAddress
    res = requests.get(URI, headers=headers)
    response = json.loads(res.text)
    return response

def getUserTxData(address, offset):
    URI = "https://public-api.solscan.io/account/exportTransactions?account="+ address + "&type=tokenchange&fromTime=" + '0' + "&toTime=" + str(offset);
    res = requests.get(URI, headers=headers)
    resCsvStr = res.text
    return resCsvStr #This is the CSV data for an Accounts Token Txs

def query_mint_authority():
    mints = []
    URI = "https://public-api.solscan.io/account/transactions?account=" + mintAuthority + "&limit=50"  
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
    mint_post = {"_id":txHash, "timeStamp":txData['blockTime'], "amount":""}
    instructions = txData['parsedInstruction']
    for parsedInstruction in instructions:
        params = parsedInstruction['params']
        try:
            if params['mint']:
                mint_post['amount'] = params['tokenAmount']['amount']
                return mint_post;  
        except:
            return None # Gracefully handling non-mint transactions from Authority

def getSingleUserTokenData(id):
    uri = f"https://public-api.solscan.io/account/tokens?account={id}"
    res = requests.get(uri, headers=headers)
    userData = json.loads(res.text)
    return userData

def getAllTxs(offset):
    print("hello")
    ## Get all txs with offset 