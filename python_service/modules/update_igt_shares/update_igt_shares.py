from modules.update_igt_shares.better_igt_calc.verification import verify_shares, validate_via_timestamps, validate_user_txs
from modules.update_igt_shares.better_igt_calc.igt_calc import igt_calc
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
    print("now 1 " + str(now))

    for holder in holders:
        validate_user_txs(holder['transactions'])
        share = igt_calc(holder['transactions'], supply_arr, now)
        if (holder["_id"] ==  "8G46LehJsszbjes5cUZ3M1kXrumiBre2cyRN22opo9HE"):
            print(share)
        total_share += share
        # myquery = { "_id": holder["_id"]}
        # newvalues = { "$set": { "igtShare": share } }
        # all_holders_collection.update_one(myquery, newvalues)
    all_txs = get_all_txs(all_holders_collection)
    #print(validate_via_timestamps(all_txs))
    print("now 2 " + str(now))
    verify_shares(total_share, supply_arr, now)

def get_all_txs(holders_col):
    holders = holders_col.find({})
    all_txs = []
    for holder in holders:
        for tx in holder['transactions']:
            all_txs.append(tx)
    return all_txs