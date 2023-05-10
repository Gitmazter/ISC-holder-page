from modules.update_igt_shares.update_igt_helpers.helpers import get_period_points, next_timestamp_function

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