from services.solscan_getters import callHoldersApi, getUserTxData
import time
from modules.update_holders.update_holder_helpers import compare_ids, get_holders, check_txs




def update_holders(all_holders_collection):
    print("updating holders...") 

    known_holders_cursor_object = all_holders_collection.find({})
    known_holders = []
    for known_holder_cursor_object in known_holders_cursor_object:
        known_holders.append(known_holder_cursor_object)

    total_number_of_holders = callHoldersApi(0)['total']
    all_holders_list = get_holders(total_number_of_holders)

    for holder in all_holders_list:
        if compare_ids(holder['owner'], known_holders) == True: 
            try:
                holder_json = {"_id": holder["owner"], 
                                "token_wallet_address": holder['address'],
                                "ignored":False,  
                                "amount": holder["amount"], 
                                "igtShare": 0.00, 
                                "igtClaimed": 0.00,
                                "transactions": []
                               }
                all_holders_collection.insert_one(holder_json)
            except:
                print("duplicate caught")

    print("successfully updated holders")


def update_user_transactions(all_holders_collection):
    print("updating user transactions... (this may take a while)")

    current_holders = all_holders_collection.find({})
    i = 0
    for holder in current_holders:
        i += 1
        if (i > 3920):
            print('updating user %s' % i)
            update_single_user_txs(holder, all_holders_collection)
    print("successfully updated user transactions")


def update_single_user_txs(holder, all_holders_collection):
    holderTokenAddress = holder["token_wallet_address"]
    holderId = holder["_id"]

    holderTxsCsv = getUserTxData(holderTokenAddress, str(round(time.time())))
    with open('./csv_files/tempTx.csv', 'w') as out:
        out.write(holderTxsCsv)
    
    myquery = { "_id": holderId}
    newvalues = { "$set": { "transactions": check_txs(holderTokenAddress) } }
    try:
        all_holders_collection.update_one(myquery, newvalues)
        print('user:: ' + holder["_id"] + ' updated')
    except:
        print('error while updating user txs')