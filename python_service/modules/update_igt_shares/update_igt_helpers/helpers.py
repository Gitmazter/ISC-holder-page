from services.solscan_getters import get_tx_data
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

def validate_all_txs(all_transactions):
    cur_time = 0
    now = time.time()

    i = 0
    while i < len(all_transactions):
        temp_tx_arr = []
        cur_time = all_transactions[i]['timeStamp']

        while all_transactions[i]['timeStamp'] == cur_time:
            temp_tx_arr.append(all_transactions[i])
            i += 1;
        
        timestamp_sum = 0
        for tx in temp_tx_arr:
            timestamp_sum += round(float(tx['amount']), 6)
        
        if timestamp_sum != 0:
            for tx in temp_tx_arr:
                print(tx)
            time.sleep(5)




    return True
