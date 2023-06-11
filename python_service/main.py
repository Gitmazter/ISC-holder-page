from pymongo import MongoClient
from services.settings import GET_KEY
from modules.update_holders.update_holders import update_holders, update_user_transactions
from modules.supply.supply import update_circulating_supply
from modules.update_igt_shares.update_igt_shares import update_igt_shares, get_single_share

# DB VARS
MONGO_DB_URL = "mongodb+srv://"+ str(GET_KEY("MONGO_DB_UN")) + ":" + str(GET_KEY("MONGO_DB_KEY")) + "@ischost.7b510c2.mongodb.net/?retryWrites=true&w=majority"
CLUSTER = MongoClient(MONGO_DB_URL)
DB = CLUSTER["ISC"]

#Collections
all_holders_collection = DB["all_holders"]
transactions_collection =  DB["all_transactions"]
supply_collection = DB["supply"]

def main():
    #update_holders(all_holders_collection)
    #update_user_transactions(all_holders_collection) ## Finished, takes long time to update, rewrite when TX database access is established
    #update_circulating_supply(all_holders_collection, supply_collection)
    update_igt_shares(all_holders_collection, supply_collection)
main()

def update_all_txs():
    print("hello")
    ## Update all txs to new mongoDB collection and implement into update users and update transactions defs