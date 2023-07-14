from modules.update_igt_shares.update_igt_shares import get_single_share
from modules.update_holders.update_holders import update_single_user_txs
from services.solscan_getters import getSingleUserTokenData
from pymongo import MongoClient
from services.settings import GET_KEY
from flask import Flask, Response, request
from flask_cors import CORS,cross_origin
import json, logging, datetime
from werkzeug.middleware.proxy_fix import ProxyFix
import logging

# GLOBAL VARS
MONGO_DB_URL = "mongodb+srv://"+ str(GET_KEY("MONGO_DB_UN")) + ":" + str(GET_KEY("MONGO_DB_KEY")) + "@ischost.7b510c2.mongodb.net/?retryWrites=true&w=majority"
CLUSTER = MongoClient(MONGO_DB_URL)
DB = CLUSTER["ISC"]

#Collections
all_holders_collection = DB["all_holders"]
supply_collection = DB["supply"]

""" FLASK STUFF """
app = Flask(__name__)
logging.basicConfig(filename='holder-page.log', level=logging.DEBUG)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)

@app.route('/igtApi/') 
@cross_origin()
def home_page():
    response = "igt Api is up and running, try /igtApi/user/?address=yourSolanaAddress"
    return json.dumps(response)

@app.route('/igtApi/user/', methods=['GET', 'POST']) 
@cross_origin()
def request_page():
    user_query = request.args.get('address') # /user/?address=yourPubKey
    holder = {}
    try:
        holder = all_holders_collection.find({ "_id" :  user_query })[0]
    except:
        holderData = getSingleUserTokenData(id=user_query)
        holderIscData = {}
        for tokenAccount in holderData:
            if tokenAccount['tokenAddress'] == "J9BcrQfX4p9D1bvLzRNCbMDv8f44a9LFdeqNE4Yk2WMD":
                holderIscData = tokenAccount

        holder_json = {
                "_id": user_query, 
                "token_wallet_address": holderIscData['tokenAccount'],
                "ignored":False,  
                "amount": holderIscData['tokenAmount']['amount'], 
                "igtShare": 0.00, 
                "igtClaimed": 0.00,
                "transactions": []
               }
        all_holders_collection.insert_one(holder_json)
        print('new user added')
        
        
    update_single_user_txs(holder, all_holders_collection)
    get_single_share(all_holders_collection, supply_collection, id=user_query)
    print('user updated')

    updated_holder = all_holders_collection.find({ "_id" :  user_query })[0]
    print(updated_holder['igtShare'])

    json_holder = json.dumps(updated_holder)
    return Response(json_holder)


if __name__ == '__main__':
    app.run(port = 8081)