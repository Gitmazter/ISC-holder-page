from classes import Event
import time

def isc_weight(total_supply, supplyArr):
    weight_time_array = []
    for event in supplyArr:
        weight_time_object = { "timeStamp": event.timeStamp, "weight":( total_supply/event.supply ) }
        weight_time_array.append(weight_time_object)
    return weight_time_array

def supply_chk(eventTime, supplyArr):
    i = 0;
    while (i+1 < len(supplyArr)):
        if (int(eventTime) > int(supplyArr[i].timeStamp) and int(eventTime) < int(supplyArr[i+1].timeStamp)):
            return supplyArr[i].supply
        i += 1
    return supplyArr[i].supply

def calculate_igt_share(holderTxs, supplyArr, weight_time_array):
    igt_share = 0.00
    holderTxs.reverse()

    holderEventArray = []
    for event in holderTxs:
        holderEventArray.append(Event(
            event['timeStamp'], 
            supply_chk(event['timeStamp'], supplyArr),
            event['newBalance']
            ))
    for event in holderEventArray:
        i = 0
        while i + 1 < len(weight_time_array):
            if int(event.timeStamp) > weight_time_array[i]["timeStamp"]  and  int(event.timeStamp) < weight_time_array[i+1]['timeStamp']:
                igt_share += get_epoch_igt_points(event, weight_time_array[i]['weight'], weight_time_array[i+1]['timeStamp'])
            i+=1;
        igt_share += get_epoch_igt_points(event, weight_time_array[i]['weight'], time.time())
    
    return(igt_share)


def get_epoch_igt_points(event, weight, epochTime):
    balance = event.balance
    print(balance)
    epoch_share = (float(balance) * (float(epochTime) - float(event.timeStamp)) / 86000) * weight
    print(epoch_share)
    time.sleep(2)
    return epoch_share


