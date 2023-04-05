from solscan_defs import callHoldersApi, callMetaApi, getUserTxData, query_mint_authority
from update_holder_services import compare_ids, get_holders
from pymongo import MongoClient
from settings import DB_KEY, IGNORED_WALLETS
import csv


# GLOBAL VARS
TOKEN_ADDRESS = "J9BcrQfX4p9D1bvLzRNCbMDv8f44a9LFdeqNE4Yk2WMD"

MONGO_DB_URL = "mongodb+srv://Phil:" + str(DB_KEY()) + "@ischost.7b510c2.mongodb.net/?retryWrites=true&w=majority"
CLUSTER = MongoClient(MONGO_DB_URL)
DB = CLUSTER["ISC"]

#Collections
all_holders_collection = DB["all_holders"]
transactions_collection =  DB["all_transactions"]
holder_ledgers_collection = DB["holder_ledgers"]
igt_share_collection = DB["igt_shares"]
supply_collection = DB["supply"]

## Place IGNORED_WALLETS in separate file that can be fetched
## when checking uncirculating supply

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
            supply_collection.insert_one(bc_mint)
            print("found new mint! Adding to list....")

    print("total supply updated successfully!")
    return metaSupply

update_coin_supply();


## Test with "2CdgwT798DG4WE6hp4PHGTG2HR5LMpyGbJNudsjdTJyw" 
# or other address(es) from files names of csv_files/user_txs in .env IGNORED_WALLETS

def update_circulating_supply():
    totalSupply = update_coin_supply();

    print("updating holder balances...")
    #update_user_transactions() ## unfinished and takes too long for testing
    print("holder balances updated successfully!")

    print("checking and updating circulating supply...")

    ## Get Ignored Wallets balances
    ignoredAmount = 0.00

    for walletAddress in IGNORED_WALLETS:
        with open('./csv_files/user_txs/'+ walletAddress +'.csv', 'r') as ignoredWalletCsv:
            reader = csv.reader(ignoredWalletCsv, delimiter=",")
            rows = list(reader)
            ignoredAmount += float(rows[1][5])

    circulatingSupply = float(totalSupply) - ignoredAmount

    print("Total Supply:  " + str(totalSupply))
    print("Uncirculating Supply:  " + str(ignoredAmount))
    print("Circulating Supply:  " + str(circulatingSupply))

    print("circulating supply updated successfully!")
    ## Return circulating supply
    return circulatingSupply

def update_user_transactions():

    iscMeta = callMetaApi()


    for holder in holder_data['data']:
        holderTokenAddress = holder['address'];
        holderWalletAddress = holder['owner'];

        # !!! NEED IGNORED_WALLETS LEDGER TO UPDATE CIRCULATING SUPPLY >> IMPLEMENT IN IGT CALC FN INSTEAD
        #if holderTokenAddress in IGNORED_WALLETS: return 0; # need to move to avoid issues

        # Deal with this when service is reliable and mostly feature complete
        ######### Check if user ledger exists, 
        ######### if it does, only request transactions after latest recorded tx 
        ######### else, record all txs

        ######### really necessary or just record all txs after latest recorded tx since
        ######### we would have already scanned the whole list of users last time? 

        holderTxsCsv = getUserTxData(holderTokenAddress)
        with open('./csv_files/tempTx.csv', 'w') as out:
            out.write(holderTxsCsv)

        userIscTxs = []

        ## Create holder tx object and remove unwanted tx's VVV
        with open('./csv_files/tempTx.csv', newline='') as csvfile:
            txreader = csv.reader(csvfile, delimiter=",")
            for row in txreader:
                if (row[9] == TOKEN_ADDRESS):
                    userIscTxs.append(row)
        
        ## then remove unwanted data and write/update permanent user ledger (only csv w/data for now, ledger later)
        ## Need to add Owner Account to send IGT! Use ISC token account for TX history! 
        with open('./csv_files/user_txs/' + holderTokenAddress + '.csv', 'w', newline='') as out:
            fieldnames = ['txHash', 'blockTimeUnix', 'changeType', 'ISC Balance Change', 'prevBalance', 'newBalance'];
            writer = csv.DictWriter(out, fieldnames=fieldnames)
            writer.writeheader()
            for row in userIscTxs:
                writer.writerow({'txHash':row[0], 'blockTimeUnix':row[1], 'changeType':row[5], 'ISC Balance Change':row[6], 'prevBalance':row[7], 'newBalance':row[8],})

        # We now have the holders TX data for all token ISC transactions: VV Bussin!
        # Now we need to read it and make a ledger for their ISC holdings: Lessgo


        # Then we can calculate their share of holdings over time to
        #calculate their share of IGT tokens

#update_circulating_supply();
#update_user_transactions();











def update_holders():
    current_holders = all_holders_collection.find({})
    total_holders = callHoldersApi(0)['total']

    holders = get_holders(total_holders)

    for holder in holders: 
        exists = compare_ids(holder['owner'], current_holders)

        if exists == False:
            holder_vson = {"_id": holder["owner"], "token_wallet_address": holder['address'],  "amount": holder["amount"]}
            all_holders_collection.insert_one(holder_vson)
 
#update_holders()  Fully working with Mongo DB






















































def calculate_igt_share(holderAddress):
    ## Calculate user holdings over time since start of quarterly epoch.
     # Should 1 second or 1 day be equal to 1 point? To simplify math?

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
    ledger = []

    with open('./csv_files/user_txs/' + holderAddress + '.csv', newline='') as csvfile:
        txreader = csv.reader(csvfile, delimiter=",")
        for row in txreader:
            ledger.append(row)

    for tx in ledger:
        print(tx)
        print("\n")

#calculate_igt_share("3NVE5ebLSnv7Gt7dQHeC7eBBorrM1xL8uc6iMypWx2j8");



 