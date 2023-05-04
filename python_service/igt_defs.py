import time

def isc_weight(total_supply, supplyArr):
    weight_time_array = []
    current_supply = 0
    for event in supplyArr:
        current_supply += int(event['amountMinted'])
        weight_time_object = { 'timeStamp': event['timeStamp'], 'weight':( total_supply/current_supply ), 'supply': current_supply }
        weight_time_array.append(weight_time_object)
    return weight_time_array

def calculate_igt_points(holder_txs, weight_time_array):
    igt_points = 0.00
    holder_txs.reverse()
    #print(weight_time_array)

    epoch_num = 0
    tx_num = 0
    while epoch_num < len(weight_time_array) and tx_num < len(holder_txs):
        account_balance = float(holder_txs[tx_num]['newBalance'])
        epoch_weight = float(weight_time_array[epoch_num]['weight'])
        
        this_tx_timestamp = int(holder_txs[tx_num]['timeStamp'])
        next_tx_timestamp = float(next_timestamp_function(tx_num, holder_txs))

        this_epoch_timestamp = int(weight_time_array[epoch_num]['timeStamp'])
        next_epoch_timestamp = float(next_timestamp_function(epoch_num, weight_time_array))

        if epoch_num + 1 == len(weight_time_array): 
            #print('calculate points until next tx for final weight value') 
            igt_points += (account_balance * ((next_tx_timestamp - this_tx_timestamp) / 86000) / epoch_weight)

        elif this_tx_timestamp > this_epoch_timestamp and this_tx_timestamp < next_epoch_timestamp:
            if next_epoch_timestamp > next_tx_timestamp:
                igt_points += ((account_balance * (next_tx_timestamp - this_tx_timestamp) / 86000) / epoch_weight)
            else:
                next_epoch_weight = float(weight_time_array[epoch_num + 1]['weight'])
                # calculate both until next epoch and after next epoch begins until next tx
                igt_points += ((account_balance * (next_epoch_timestamp - this_tx_timestamp) / 86000) / epoch_weight)
                igt_points += ((account_balance * (next_tx_timestamp - next_epoch_timestamp) / 86000) / next_epoch_weight)
                epoch_num += 1
            
        else:
            #print('transaction occured after current epoch')
            epoch_num += 1
        tx_num += 1

    return igt_points

def get_total_igt_points(weight_time_array):
    total_points = 0
    mint_num = 0
    while mint_num < len(weight_time_array):
        print(weight_time_array[mint_num]['supply'])
        supply = weight_time_array[mint_num]['supply'] / 1000000
        epoch_weight = float(weight_time_array[mint_num]['weight'])

        this_mint_timestamp = weight_time_array[mint_num]['timeStamp']
        next_mint_timestamp = next_timestamp_function(mint_num, weight_time_array)

        total_points += ((supply * (next_mint_timestamp - this_mint_timestamp) / 86000) / epoch_weight)

        mint_num += 1
    return total_points

def next_timestamp_function(event_num, event_array):
    if event_num + 1 == len (event_array):
        return time.time()
    else:
        return event_array[event_num + 1]['timeStamp']



