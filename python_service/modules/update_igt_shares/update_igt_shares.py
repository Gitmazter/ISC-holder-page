from modules.update_igt_shares.better_igt_calc.igt_calc import igt_calc, get_total_igt
import time

def update_igt_shares(circulating_supply, all_holders_collection, supply_collection):
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
    

