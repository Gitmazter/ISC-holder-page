import time

def isc_weight(total_supply, supplyArr):
    weight_time_array = []
    current_supply = 0
    for event in supplyArr:
        current_supply += float(event['amount'])
        weight_time_object = { 'timeStamp': event['timeStamp'], 'weight':( current_supply/total_supply ), 'supply': current_supply }
        weight_time_array.append(weight_time_object)
    return weight_time_array



def get_period_points(balance, time_stamp_1, time_stamp_2, weight):  
    points = (((balance * (int(time_stamp_1) - int(time_stamp_2))) / 86400) / weight)
    return points



def next_timestamp_function(event_num, event_array):
    if event_num + 1 == len (event_array):
        return time.time()
    else:
        return event_array[event_num + 1]['timeStamp']
    


def calculate_igt_points(holder_txs, weight_time_array):
    igt_points = 0.00
    holder_txs.reverse()
    #print(weight_time_array)

    epoch_num = 0
    tx_num = 0

    while tx_num < len(holder_txs):
        account_balance = float(holder_txs[tx_num]['newBalance'])
        epoch_weight = float(weight_time_array[epoch_num]['weight'])
        
        this_tx_timestamp = int(holder_txs[tx_num]['timeStamp'])
        next_tx_timestamp = float(next_timestamp_function(tx_num, holder_txs))
        this_epoch_timestamp = int(weight_time_array[epoch_num]['timeStamp'])
        next_epoch_timestamp = float(next_timestamp_function(epoch_num, weight_time_array))

        if epoch_num + 1 == len(weight_time_array): 
            # No new epochs after current tx
            igt_points += get_period_points(account_balance, next_tx_timestamp, this_tx_timestamp, epoch_weight)
            # increment Tx
            tx_num += 1

        elif this_tx_timestamp >= this_epoch_timestamp and this_tx_timestamp < next_epoch_timestamp:
        # transaction occured at or after beginning of this epoch until end of epoch

            if next_tx_timestamp <= next_epoch_timestamp:
                #  Next transaction occured before or at the moment of next epoch start
                igt_points += get_period_points(account_balance, next_tx_timestamp, this_tx_timestamp, epoch_weight)
                # increment Tx
                tx_num += 1

            else:
                # Next transaction occured after next epoch start

                # Count points until end of current epoch
                igt_points += get_period_points(account_balance, next_epoch_timestamp, this_tx_timestamp, epoch_weight)

                # If next tx occurs after an uneventful epoch(s), add points for this/those epoch(s)
                while next_tx_timestamp > next_epoch_timestamp:
                    # increment epoch and update vars
                    epoch_num += 1
                    epoch_weight = float(weight_time_array[epoch_num]['weight'])
                    this_epoch_timestamp = int(weight_time_array[epoch_num]['timeStamp'])
                    next_epoch_timestamp = float(next_timestamp_function(epoch_num, weight_time_array))

                    # check if next_tx occured outside after epoch indicating an uneventful epoch
                    if next_tx_timestamp > next_epoch_timestamp:
                        igt_points += get_period_points(account_balance, next_epoch_timestamp, this_epoch_timestamp, epoch_weight)

                # Calculate points until next tx from start of final epoch
                igt_points += get_period_points(account_balance, next_tx_timestamp, this_epoch_timestamp, epoch_weight)
                # increment Tx
                tx_num += 1

        else:
            # Transaction occured after current epoch, increment epoch
            epoch_num += 1

    return igt_points



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