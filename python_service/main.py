from solscan_defs import callHoldersApi, callMetaApi, getUserTxData, query_mint_authority
from update_holder_services import compare_ids, get_holders, check_txs
from pymongo import MongoClient
from settings import GET_KEY
from classes import Event
from igt_defs import isc_weight, calculate_igt_share
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
    fetched_known_holders = all_holders_collection.find({})
    known_holders = []
    for fetched_known_holder in fetched_known_holders:
        known_holders.append(fetched_known_holder)

    total_number_of_holders = callHoldersApi(0)['total']
    holder_list = get_holders(total_number_of_holders)

    for holder in holder_list:
        if compare_ids(holder['owner'], known_holders) == True: 
            try:
                holder_json = {"_id": holder["owner"], "token_wallet_address": holder['address'], "ignored":False,  "amount": holder["amount"], "IgtShare": 0.00, "transactions": []}
                all_holders_collection.insert_one(holder_json)
            except:
                print("duplicate caught")

    print("successfully updated holders")

def update_coin_supply():
    print("checking and updating total supply...")

    coin_meta_data = callMetaApi()
    metaSupply = coin_meta_data['supply']; 

    bc_mints = query_mint_authority();
    db_mints = supply_collection.find({})

    fetchSupply = 0;
    for bc_mint in bc_mints:
        fetchSupply += int(bc_mint["amountMinted"])

    print("before: " +str(fetchSupply) + "  Now: " + metaSupply) ##  THERE IS BURN!!

    for bc_mint in bc_mints:
        if compare_ids(bc_mint['_id'], db_mints) == False:
            print("found new mint! Adding to list....")
            supply_collection.insert_one(bc_mint)

    print("total supply updated successfully!")
    return metaSupply


def update_circulating_supply():
    totalSupply = update_coin_supply();
    print("checking and updating circulating supply...")
    holders = all_holders_collection.find({})

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

        try:
            all_holders_collection.update_one(myquery, newvalues)
            print('user updated')
        except:
            print('error while updating user txs')
        time.sleep(0.2) # To account for Solscan limits
    print("successfully updated user transactions")







def update_igt_shares(circulating_supply):
    print("Calculating User IGT Shares")
    
    holders = all_holders_collection.find({})
    supply_cursor_object = supply_collection.find({})
    
    supplyArr = []
    for supply in supply_cursor_object:
        supplyArr.append(supply)
    supplyArr.reverse()

    total_supply = 0
    supplyEventArr = []

    for event in supplyArr:
        total_supply += int(event["amountMinted"])
        supplyEventArr.append(Event(event['timeStamp'], total_supply, 0))
    
    weightArr = isc_weight(total_supply, supplyEventArr)

    for holder in holders:
        calculate_igt_share(holder['transactions'], supplyEventArr, weightArr)
        # myquery = { "_id": holder["_id"]}
        # newvalues = { "$set": { "igtShare": calculate_igt_share(holder, supplyArr) } }

        # all_holders_collection.update_one(myquery, newvalues)

    print("All IGT Shares Updated")

def main():
    update_holders()
    #update_user_transactions() ## Finished, takes long time to update
    #circulating_supply = update_circulating_supply()
    #update_igt_shares(circulating_supply)
main()





## Calculate user holdings over time since start of quarterly epoch.
 # Should 1 second or 1 day be equal to 1 point? To simplify math?
 # Ignore wallets with holder["ignored"] = true
""" 
Method: 
    Example 1:
        If a holder holds 1 ISC for 1 UNIX day, 86400 seconds, they now have 1(or 86400) hold point(s)
        the hold point divided by current supply will equal their share IGT accrued for that day
        example: 
        It is exactly 60 days since launch of ISC
        Holder buys and holds 200 ISC tokens for 30(* 86400 seconds (unix)) days thus accumulating 6000 hold points
        during this time the circulating supply stays the same and thus the total hold points to be distributed equals:
        230.000 * 90(* 86400 seconds (unix)) = 20.700.000
        as the holder has 6000 points accrued while holding, their share of IGT will equal:
        6000 / 20.700.000 = 0.0002898550 (Decimals continue but will be rounded to smallest IGT decimal)
        therefore if 1.000.000 IGT will be distributed, this holder will receive (share * IGT supply): 289.85507246 IGT
        
    Example 2 (supply change):
        following the previous example but adding a supply change during the quarter,
        trying to be as accurate as possible:
        this quarter consists of 91.5 days = 7,905,600 seconds
        the total supply for the first 42 days and 39,000 seconds is : 230000 ISC
        (the total seconds for this time span is: 3,667,800)
        (total seconds for second supply span is 4,237,800 seconds)
        at this exact time a block is created where a transaction mints 215000ISC making the total supply 435000ISC
        A holder buys 3251 ISC on day 31 and 41000 seconds into the quarter then holds it until 
        86400 seconds(1 day) of the quarter is remaining. (the holder buys ISC at second 2,719,400)
        How many IGT will he receive if 1,000,000 IGT will be distributed? :
        1st time span consists of ( 3,667,800 * 230,000 ISC points ) :: 843,594,000,000
        2nd time span consists of (4,237,800 * 435,000 ISC points) :: 1,843,443,000,000
        the holder holds 3251 ISC for the final (3,667,800 - 2,719,400 )= 948,400 seconds of the first time span
        earning(time * held ISC): 3,083,248,400 ISC points out of a total 843,410,000,000
        for the second time span the holder holds for (4,236,800 - 86400(to account for sale))= 4,150,400sec and earns
        (time * held ISC): 13,492,950,400
        since the holdings during the first time span held a greater weight, we account for this by factoring in 
        the supply change by multiplying all previous points by 435000/230000 = ~1.8913
        so the users total points are now: (3,083,248,400 * 1.8913) + 13,492,950,400 = 19,324,298,098.92
        and the total ISC points are now: (1st span * 1.8913) 1,595,489,332,200 + 2nd span = 3,438,932,332,200
        the users total IGT share is now = user points / total points * IGT supply = 5,619.272562 IGT

"""
#The quarter ends by starting new holder ledgers after a set time or when a mint/send Tx is detected by IGT Token Account 
#Thought, do holder points carry over to next quarter or reset?




 