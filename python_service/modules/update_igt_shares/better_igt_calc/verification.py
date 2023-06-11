from modules.update_igt_shares.better_igt_calc.igt_calc import get_total_igt
import time

def get_time(tx):
    return tx['timeStamp']


def verify_shares(total_share, supply_arr, now):
    total_igt = get_total_igt(supply_arr, now)
    print(total_share)
    print(total_igt)

    if total_share - total_igt < 1 and total_share - total_igt > -1:
        print("shares verified with a tolerance of 2 points")





def validate_via_timestamps(all_transactions):
    sorted_transactions = sorted(all_transactions, key=get_time)
    are_txs_valid = validate_all_txs(sorted_transactions)
    return are_txs_valid



def validate_all_txs(all_transactions):
    time_stamp_list = []
    grand_sum = 0

    for tx in all_transactions:
        timestamp = tx['timeStamp']
        try:
            time_stamp_list.index(timestamp)
        except:
            time_stamp_list.append(timestamp)
        
    for time_stamp in time_stamp_list:
        def compare_timestamp(tx):
            if tx['timeStamp'] == time_stamp:
                return True
            else:
                return False

        filtered_block_txs = filter(compare_timestamp, all_transactions)
        block_txs = list(filtered_block_txs)
        block_sum = 0.00;
        for tx in block_txs:
            amount = float(tx['amount'])
            block_sum += amount 

        if block_sum == 0:
            print('Transactions for block minded at ', str(time_stamp), ' are valid sum : ', str(block_sum))
        else:
             print('Transactions for block minded at ', str(time_stamp), ' are Invalid! sum : ', str(block_sum))
        grand_sum += block_sum

    print(" GRAND _ SUM ==== ", grand_sum)
    return grand_sum


def validate_user_txs(holder_transactions):
    holder_transactions.reverse()
    expected_balance = 0.00
    for tx in holder_transactions:
        expected_balance += float(tx['amount'])

    expected_balance = round(expected_balance, 6)
    actual_balance = float(holder_transactions[len(holder_transactions)-1]['newBalance'])
    
    if actual_balance != expected_balance and actual_balance != 0:
        print("expected_balance: ", expected_balance, " Actual Balance: ",  holder_transactions[len(holder_transactions)-1]['newBalance'])
        return False
    else:
        #print('user txs are valid')
        return True