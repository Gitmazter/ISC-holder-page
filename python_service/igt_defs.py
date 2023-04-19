from classes import Event
import time

def isc_weight(total_supply, supplyArr):
    weightArr = []
    for event in supplyArr:
        weightObject = {"timeStamp": event.timeStamp, "weight":(total_supply/event.supply)}
        weightArr.append(weightObject)
    return weightArr

def supply_chk(eventTime, supplyArr):
    i = 0;
    while (i+1 < len(supplyArr)):
        if (int(eventTime) > int(supplyArr[i].timeStamp) and int(eventTime) < int(supplyArr[i+1].timeStamp)):
            return supplyArr[i].supply
        i += 1
    return supplyArr[i].supply

def calculate_igt_share(holderTxs, supplyArr, weightArr):
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
            while i + 1 < len(weightArr):
                #print("range condition met")
                if int(event.timeStamp) > weightArr[i]["timeStamp"] and int(event.timeStamp) < weightArr[i+1]['timeStamp']:
                    #print("event time is greater than weight epoch and is less than the time of the next epoch")
                    igt_share += get_epoch_igt_points(event, weightArr[i]['weight'], weightArr[i+1]['timeStamp'])
                i+=1;
            #print("user event took place after latest mint")
            igt_share += get_epoch_igt_points(event, weightArr[i]['weight'], time.time())
    print("this is the Share    " + str(igt_share))
    
    return(igt_share)


def get_epoch_igt_points(event, weight, epochTime):
    balance = event.balance
    epoch_share = (float(balance) * (float(epochTime) - float(event.timeStamp)) / 86000) * weight
    return epoch_share


