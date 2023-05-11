from modules.update_igt_shares.update_igt_helpers.helpers import isc_weight
from modules.update_igt_shares.update_igt_helpers.calculate_igt_points import calculate_igt_points
from modules.update_igt_shares.update_igt_helpers.get_total_igt_points import get_total_igt_points

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

    for holder in holders:
        share = calculate_igt_points(holder['transactions'], weight_time_array)
        remaining_igt_points -= share

        myquery = { "_id": holder["_id"]}
        newvalues = { "$set": { "igtShare": share } }
        #all_holders_collection.update_one(myquery, newvalues)
    print(total_igt_points)
    print(remaining_igt_points)
