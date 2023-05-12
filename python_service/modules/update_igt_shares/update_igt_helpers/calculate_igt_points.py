from modules.update_igt_shares.update_igt_helpers.helpers import get_period_points, next_timestamp_function


from modules.supply.supply_helpers import sort_in_event

# Try not to use floats, decimals package works


def calculate_igt_points(holder_txs, weight_time_array):
    igt_points = 0.00
    holder_txs.reverse()

    print(holder_txs[0])
    print(weight_time_array[0])
    
    make_weighted_txs(holder_txs, weight_time_array)



    tx_num = 0
    # while tx_num < len(holder_txs):
    #     print()

    return igt_points

def make_weighted_txs():
    weighted_tx_array 
