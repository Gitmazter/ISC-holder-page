from modules.update_igt_shares.update_igt_helpers.helpers import isc_weight, validate_all_txs
from modules.update_igt_shares.update_igt_helpers.calculate_igt_points import calculate_igt_points
from modules.update_igt_shares.update_igt_helpers.get_total_igt_points import get_total_igt_points
from modules.update_holders.update_holder_helpers import validate_user_txs

def update_igt_shares(circulating_supply, all_holders_collection, supply_collection):
    holders = all_holders_collection.find({})
    supply_cursor_object = supply_collection.find({})
    
    supply_arr = []
    for supply in supply_cursor_object:
        supply_arr.append(supply)
    supply_arr.reverse()

    weight_time_array = isc_weight(circulating_supply, supply_arr)
    total_igt_points = get_total_igt_points(weight_time_array)
    remaining_igt_points = total_igt_points
    sum_supply = 0
    all_transactions = []
    for holder in holders:
        
        validate_user_txs(holder['transactions'])
        for tx in holder['transactions']:
            all_transactions.append(tx)

        share = calculate_igt_points(holder['transactions'], weight_time_array)
        remaining_igt_points -= share

        myquery = { "_id": holder["_id"]}
        newvalues = { "$set": { "igtShare": share } }
        #all_holders_collection.update_one(myquery, newvalues)
    
    #validate_via_timestamps(all_transactions)
    # print(total_igt_points)
    # print(remaining_igt_points)
    print(total_igt_points)
    print(remaining_igt_points)

def get_time(tx):
    return tx['timeStamp']

def validate_via_timestamps(all_transactions):
    #earliest_timestamp = find_earliest_timestamp(all_transactions)
    sorted_transactions = sorted(all_transactions, key=get_time)
    are_txs_valid = validate_all_txs(sorted_transactions)


def find_earliest_timestamp(all_transactions):
    earliest = int(all_transactions[0]['timeStamp'])
    print(len(all_transactions))
    for tx in all_transactions:
        if earliest > int(tx['timeStamp']):
            earliest = int(tx['timeStamp'])
    
    print('earliest timestamp:' + str(earliest))

    return earliest
