from modules.update_igt_shares.better_igt_calc.igt_calc import igt_calc, get_total_igt
import time

def update_igt_shares(all_holders_collection, supply_collection):
    holders = all_holders_collection.find({})
    supply_cursor_object = supply_collection.find({})
    
    supply_arr = []
    for supply in supply_cursor_object:
        supply_arr.append(supply)
    supply_arr.reverse()

    total_share = 0
    now = time.time()
    for holder in holders:
        share = igt_calc(holder['transactions'], supply_arr, now)
        total_share += share
        myquery = { "_id": holder["_id"]}
        newvalues = { "$set": { "igtShare": share } }
        all_holders_collection.update_one(myquery, newvalues)
    verify_shares(total_share, supply_arr, now)


def verify_shares(total_share, supply_arr, now):
    total_igt = get_total_igt(supply_arr, now)
    print(total_share)
    print(total_igt)

    if total_share - total_igt < 1 and total_share - total_igt > -1:
        print("shares verified with a tolerance of 2 points")



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
