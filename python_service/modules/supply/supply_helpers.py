def add_burn_events(event_array, holders_col):
    # no burns in user transactions after testing
    # Write this when access to all tx database is established
    return event_array

def sort_in_event(event, temp_event_array):
    event_num = 0
    while int(event['timeStamp']) < int(temp_event_array[event_num]['timeStamp']):
        event_num += 1 #This is the position for our event
    temp_event_array.insert(event_num, event)
    return temp_event_array
    
def add_ignored_wallets_events(event_array, user_mongo_col):
    users = user_mongo_col.find({})
    temp_event_array = event_array

    for user in users:
        if (user['ignored'] == True):
            for tx in user['transactions']:
                print(tx)
                tx_event_object = {"_id":tx['tx_hash'], "timeStamp":tx['timeStamp'], "amount":tx['amount']}
                temp_event_array = sort_in_event(tx_event_object, event_array)

    return temp_event_array