from flask import *
import json, time
from modules.update_igt_shares.update_igt_shares import get_single_share
from pymongo import MongoClient
from services.settings import GET_KEY

# GLOBAL VARS
MONGO_DB_URL = "mongodb+srv://"+ str(GET_KEY("MONGO_DB_UN")) + ":" + str(GET_KEY("MONGO_DB_KEY")) + "@ischost.7b510c2.mongodb.net/?retryWrites=true&w=majority"
CLUSTER = MongoClient(MONGO_DB_URL)
DB = CLUSTER["ISC"]

#Collections
all_holders_collection = DB["all_holders"]
supply_collection = DB["supply"]



app = Flask(__name__)

@app.route('/', methods=['GET'])
def home_page():
    data_set ={'Page' : "Home", "Message" : "Fully Loaded The Home Page", "Timestamp" : time.time()}
    json_dump = json.dumps(data_set)

    return json_dump

@app.route('/igtBalance/', methods=['GET'])
def request_page():
    user_query = str(request.args.get('address')) # /user/?address=yourPubKey
    user_balance = get_single_share(all_holders_collection, supply_collection, id=user_query)

    data_set = {"Page" : "igtBalance", "Message" : f"User igt balance {user_balance}", "Timestamp" : time.time() }    
    json_dump = json.dumps(data_set)

    return json_dump


if __name__ == '__main__':
    app.run(port=7777)