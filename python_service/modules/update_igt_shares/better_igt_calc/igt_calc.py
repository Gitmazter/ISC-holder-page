from modules.update_igt_shares.better_igt_calc.Event import Event
igt_per_second = 1000000 / 30.5 / 86400

def getTime(e):
    return str(e['timeStamp'])

def igt_calc(user_transactions, supply_array, now):
    igt_owed = 0

    event_array = make_event_array(user_transactions, supply_array, now)

    event_range = range( 0, len(event_array) - 1 )
    for i in event_range:
        igt_owed += get_igt(event_array[i], event_array[i + 1])
    return(igt_owed)

def get_igt(tx1, tx2):
    igt_per_isc_per_second = igt_per_second / tx1.supply
    timespan = int(tx2.timestamp) - int(tx1.timestamp)

    igt = tx1.balance * igt_per_isc_per_second * timespan
    return igt

def make_event_array(user_transactions, supply_array, now):
    temp_array = user_transactions

    # break this out to global var for speed
    for event in supply_array:
        temp_array.append(event)
    temp_array.sort(key=getTime)

    event_array = convert_array(temp_array, now)

    return event_array

def convert_array(temp_array, now):
    supply = 0.000001 ## only works if supply starts at 0.000001 for some users, else div by 0 fault
    balance = 0
    converted_array = []

    for event in temp_array:
        try: 
            balance = float(event['newBalance']) * 1e6
        except:
            supply += int(event['amount'])
        converted_array.append(Event(event['timeStamp'], balance, supply))
    # dummy tx to cap array
    converted_array.append(Event(now, balance, supply))

    return converted_array

def get_total_igt(supply_array, now):
    start_time = supply_array[0]['timeStamp']
    time_since_launch = now - start_time
    total_igt = igt_per_second * time_since_launch
    return total_igt