from modules.update_igt_shares.update_igt_shares import get_single_share
from pymongo import MongoClient
from services.settings import GET_KEY
from flask import Flask, Response, request, jsonify
from flask_cors import CORS
from flask_ngrok import run_with_ngrok
import time, json, logging


# GLOBAL VARS
MONGO_DB_URL = "mongodb+srv://"+ str(GET_KEY("MONGO_DB_UN")) + ":" + str(GET_KEY("MONGO_DB_KEY")) + "@ischost.7b510c2.mongodb.net/?retryWrites=true&w=majority"
CLUSTER = MongoClient(MONGO_DB_URL)
DB = CLUSTER["ISC"]

#Collections
all_holders_collection = DB["all_holders"]
supply_collection = DB["supply"]

""" FLASK STUFF """
app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logging.getLogger('flask_cors').level = logging.DEBUG
CORS(app, resources={r"/*": {"origins": "*"}})
run_with_ngrok(app)

@app.route('/', methods=['POST'])
def home_page():
    data_set = '{"hallo":"world","I":"Am","Timestamp":%s}' % (time.time())
    response = Response(str(data_set))
    return response

@app.route('/user/', methods=['POST']) 
def request_page():
    user_query = request.args.get('address') # /user/?address=yourPubKey
    # user = user_query
    # user_balance = get_single_share(all_holders_collection, supply_collection, id=user_query)
    # data_set = '{"User": "%s" ,"IGT_balance":%s,"Timestamp":%s}' % (user, user_balance, time.time())
    
    user = get_single_share(all_holders_collection, supply_collection, id=user_query)
    json_user = json.dumps(user)
    return Response(json_user)


if __name__ == '__main__':
    app.run()