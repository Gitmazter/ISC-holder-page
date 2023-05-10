from modules.update_igt_shares.update_igt_helpers.helpers import get_period_points, next_timestamp_function

def get_total_igt_points(weight_time_array):
    total_points = 0
    mint_num = 0
    while mint_num < len(weight_time_array):

        supply = weight_time_array[mint_num]['supply'] / 1000000
        epoch_weight = float(weight_time_array[mint_num]['weight'])

        this_mint_timestamp = weight_time_array[mint_num]['timeStamp']
        next_mint_timestamp = next_timestamp_function(mint_num, weight_time_array)

        total_points += get_period_points(supply, next_mint_timestamp, this_mint_timestamp, epoch_weight)

        mint_num += 1
    return total_points