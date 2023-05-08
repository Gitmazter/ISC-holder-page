from solscan_defs import callHoldersApi, callMetaApi, getUserTxData, query_mint_authority
from update_holder_services import compare_ids, get_holders, check_txs
from pymongo import MongoClient
from settings import GET_KEY
from classes import Event
from igt_defs import isc_weight, calculate_igt_points, get_total_igt_points
import time

# GLOBAL VARS
TOKEN_ADDRESS = "J9BcrQfX4p9D1bvLzRNCbMDv8f44a9LFdeqNE4Yk2WMD"

MONGO_DB_URL = "mongodb+srv://"+ str(GET_KEY("MONGO_DB_UN")) + ":" + str(GET_KEY("MONGO_DB_KEY")) + "@ischost.7b510c2.mongodb.net/?retryWrites=true&w=majority"
CLUSTER = MongoClient(MONGO_DB_URL)
DB = CLUSTER["ISC"]

#Collections
all_holders_collection = DB["all_holders"]
transactions_collection =  DB["all_transactions"]
supply_collection = DB["supply"]

## Place IGNORED_WALLETS in separate file that can be fetched
## when checking non-circulating supply

def update_holders():
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
                holder_json = {"_id": holder["owner"], "token_wallet_address": holder['address'], "ignored":False,  "amount": holder["amount"], "IgtShare": 0.00, "transactions": []}
                all_holders_collection.insert_one(holder_json)
            except:
                print("duplicate caught")

    print("successfully updated holders")


def add_burn_events(event_array, holders_col):
    # no burns in user transactions after testing
    # Write this when access to all tx database is established
    return event_array

def sort_in_event(event, event_array):
    event_num = 0
    while int(event['timeStamp']) < int(event_array[event_num]['timeStamp']):
        event_num += 1
        #### LEFT OFF HERRE

def add_ignored_wallets_events(event_array, user_mongo_col):
    users = user_mongo_col.find({})
    temp_event_array = event_array

    for user in users:
        if (user['ignored'] == True):
            for tx in user['transactions']:
                temp_event_array = sort_in_event(tx, event_array)

    return temp_event_array


def update_coin_supply():
    print("checking and updating total supply...")

    coin_meta_data = callMetaApi()
    metaSupply = coin_meta_data['supply']; 
    
    mint_event_array = query_mint_authority();

    mints_and_ignored_wallet_event_array = add_ignored_wallets_events(mint_event_array, all_holders_collection)

    mints_and_ignored_wallets_and_burns_event_array = add_burn_events(mints_and_ignored_wallet_event_array, all_holders_collection)

    supply_events_cursor_object = supply_collection.find({})
    db_supply_events_array = []
    for supply_event_in_cursor_object in supply_events_cursor_object:
        db_supply_events_array.append(supply_event_in_cursor_object)

    fetchSupply = 0;
    for mint in mints_and_ignored_wallets_and_burns_event_array:
        fetchSupply += int(mint["amountMinted"])

    print("before: " +str(fetchSupply) + "  Now: " + metaSupply) ##  THERE IS BURN!!

    for event in mints_and_ignored_wallets_and_burns_event_array:
        new_event = True
        for db_mint in db_supply_events_array:
            if event["_id"] == db_mint["_id"]:
                new_event = False
        if new_event == True:
            print("found new event! Adding to list....")
            #supply_collection.insert_one(event)

    print("total supply updated successfully!")
    return metaSupply


def update_circulating_supply():
    totalSupply = update_coin_supply();
    print("checking and updating circulating supply...")

    fetched_holders = all_holders_collection.find({})
    holders = []
    for fetched_holder in fetched_holders:
        holders.append(fetched_holder)

    ## Get Ignored Wallets balances
    ignoredAmount = 0.00

    for holder in holders:
        if (holder["ignored"] == True):
            ignoredAmount += holder["amount"]

    circulatingSupply = float(totalSupply) - ignoredAmount

    print("Total Supply:  " + str(totalSupply))
    print("Uncirculating Supply:  " + str(ignoredAmount))
    print("Circulating Supply:  " + str(circulatingSupply))

    print("circulating supply updated successfully!")
    return circulatingSupply


def update_user_transactions():
    print("updating user transactions... (this may take a while)")

    current_holders = all_holders_collection.find({})

    for holder in current_holders:
        holderTokenAddress = holder["token_wallet_address"]
        holderId = holder["_id"]

        holderTxsCsv = getUserTxData(holderTokenAddress)
        with open('./csv_files/tempTx.csv', 'w') as out:
            out.write(holderTxsCsv)

        myquery = { "_id": holderId}
        newvalues = { "$set": { "transactions": check_txs() } }
        i = 0
        try:
            all_holders_collection.update_one(myquery, newvalues)
            i += 1
            print('user no ' + str(i) + ' updated')
        except:
            print('error while updating user txs')
        time.sleep(0.1) # To account for Solscan limits
    print("successfully updated user transactions")

def update_all_txs():
    print("hello")
    ## Update all txs to new mongoDB collection and implement into update users and update transactions defs

def update_igt_shares(circulating_supply):
    holders = all_holders_collection.find({})
    supply_cursor_object = supply_collection.find({})
    
    supply_arr = []
    for supply in supply_cursor_object:
        supply_arr.append(supply)
    supply_arr.reverse()

    weight_time_array = isc_weight(circulating_supply, supply_arr)
    total_igt_points = get_total_igt_points(weight_time_array)

    for holder in holders:
        share = calculate_igt_points(holder['transactions'], weight_time_array)
        total_igt_points -= share

        # myquery = { "_id": holder["_id"]}
        # newvalues = { "$set": { "igtShare": calculate_igt_share(holder, supplyArr) } }
    print(total_igt_points)
    #     # all_holders_collection.update_one(myquery, newvalues)
    # print(total_points)
    # print("All IGT Shares Updated")

def main():
    #update_holders()
    #update_user_transactions() ## Finished, takes long time to update
    circulating_supply = update_circulating_supply()
    #update_igt_shares(circulating_supply)
main()
