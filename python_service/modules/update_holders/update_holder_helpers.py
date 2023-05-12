from services.solscan_getters import callHoldersApi, getUserTxData
from services.settings import GET_KEY
import csv 

# checks if holder matches or already in database
def compare_ids(id, holder_arr):
    new_user = True
    for holder in holder_arr:
        if id == holder["_id"]:
            new_user = False
    return new_user

# add all txs to an array and sum for each timestamp
# it should add up to 0 if correct since all txs need an enpoint except mints

# gets all holders from solscan
def get_holders(total_holders):
        print("total holders:" + str(total_holders))
        holders = []
        offset = 0

        while offset < total_holders:
            print("offset " + str(offset)) 
            for holder in callHoldersApi(offset)['data']:
                holders.append(holder)
            offset += 50
        
        return holders

def validate_user_txs(holder_transactions):
    holder_transactions.reverse()
    expected_balance = 0.00
    for tx in holder_transactions:
        expected_balance += float(tx['amount'])

    expected_balance = round(expected_balance, 6)
    if float(holder_transactions[len(holder_transactions)-1]['newBalance']) != expected_balance:
        print("expected_balance: ", expected_balance, " Actual Balance: ",  holder_transactions[len(holder_transactions)-1]['newBalance'])

def check_txs(holderTokenAddress):
    newTxs = []
    tokenAddress = GET_KEY("TOKEN_ADDRESS")
    with open('./csv_files/tempTx.csv', newline='') as csvfile:
        txreader = csv.reader(csvfile, delimiter=",")
        for row in txreader:
            if (row[9] == tokenAddress):
                tx = {"tx_hash": row[0], "timeStamp":row[1], "type": row[5], "amount":row[6], "newBalance": row[8]}
                newTxs.append(tx)
    if len(newTxs) == 5000:
        print('over 5000 txs')
        newTxs = busy_account(holderTokenAddress, newTxs, tokenAddress)
        
    return newTxs

def busy_account(holderTokenAddress, newTxs, tokenAddress):
    ## overlap 1 timestamp sec and verify in between txs 
    num_txs = 5000
    i = 1
    while num_txs / 5000 == i:
        offset = int(newTxs[len(newTxs)-1]['timeStamp']) + 1   
        temp_txs = []
        holderTxsCsv = getUserTxData(holderTokenAddress, offset)
        with open('./csv_files/tempTx.csv', 'w') as out:
            out.write(holderTxsCsv)
        
        with open('./csv_files/tempTx.csv', newline='') as csvfile:
            txreader = csv.reader(csvfile, delimiter=",")
            for row in txreader:
                if (row[9] == tokenAddress):
                    tx = {"tx_hash": row[0], "timeStamp":row[1], "type": row[5], "amount":row[6], "newBalance": row[8]}
                    temp_txs.append(tx)

        for tx in temp_txs:
            try: 
                newTxs.index(tx) 
                print('found dupe')
            except: newTxs.append(tx)
        num_txs += len(temp_txs)
        i += 1
    print(len(newTxs))

    return newTxs