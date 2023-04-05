from solscan_defs import callHoldersApi


# checks if holder matches on already in database
def compare_ids(id, dict_array_with_ids):
    for current_dict in dict_array_with_ids:
        if id == current_dict['_id']:
            return True
    return False

# gets all holders from solscan
def get_holders(total_holders):
        holders = []
        offset = 0

        while offset < total_holders: 
            for holder in callHoldersApi(offset)['data']:
                holders.append(holder)
            offset += 50
        
        return holders