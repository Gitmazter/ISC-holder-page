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