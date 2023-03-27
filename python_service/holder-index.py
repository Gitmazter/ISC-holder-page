from solscan_defs import callHoldersApi, callMetaApi, getUserTxData
import csv
import pandas

TOKEN_ADDRESS = "J9BcrQfX4p9D1bvLzRNCbMDv8f44a9LFdeqNE4Yk2WMD"
IGNORED_WALLETS = [];

def update_ledgers():
    holderData = callHoldersApi()
    iscMeta = callMetaApi()
    print(iscMeta)

    for holder in holderData['data']:
        holderAddress = holder['address']
        if holderAddress in IGNORED_WALLETS: return 0;

        # Deal with this when service is reliable and mostly feature complete
        ######### Check if user ledger exists, 
        ######### if it does, only request transactions after latest recorded tx 
        ######### else, record all txs

        ######### really necessary or just record all txs after latest recorded tx since
        ######### we would have already scanned the whole list of users last time? 

        holderTxsCsv = getUserTxData(holderAddress)
        with open('./csv_files/tempTx.csv', 'w') as out:
            out.write(holderTxsCsv)

        userIscTxs = []

        with open('./csv_files/tempTx.csv', newline='') as csvfile:
            txreader = csv.reader(csvfile, delimiter=",")
            for row in txreader:
                if (row[9] == TOKEN_ADDRESS):
                    userIscTxs.append(row)
        
        with open('./csv_files/user_ledgers/' + holderAddress + '.csv', 'w') as out:
            for row in userIscTxs:
                out.write("\n")
                for item in row:
                    out.write(item + ",")
            

        ## Create holder tx object and remove unwanted tx's

        ## then remove unwanted data and write/update permanent user ledger

        # We now have the holders TX data for all token ISC transactions

        # Now we need to read it and make a ledger for their ISC holdings




        # Then we can calculate their share of holdings over time to
        #calculate their share of IGT tokens

update_ledgers()


 