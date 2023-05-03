from solscan_defs import callHoldersApi
import csv 
TOKEN_ADDRESS = "J9BcrQfX4p9D1bvLzRNCbMDv8f44a9LFdeqNE4Yk2WMD"

# checks if holder matches or already in database
def compare_ids(id, holder_arr):
    new_user = True
    for holder in holder_arr:
        if id == holder["_id"]:
            new_user = False
    return new_user


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

def check_txs():
    newTxs = []
    with open('./csv_files/tempTx.csv', newline='') as csvfile:
        txreader = csv.reader(csvfile, delimiter=",")
        for row in txreader:
            if (row[9] == TOKEN_ADDRESS):
                tx = {"tx_hash": row[0], "timeStamp":row[1], "type": row[5], "amount":row[6], "newBalance": row[8]}
                newTxs.append(tx)
    return newTxs