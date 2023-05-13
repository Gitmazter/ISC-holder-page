# # event objects
# tx {bal, supply, timestamp}
# tx
# tx
# tx
# tx {bal, supply, timestamp}
# supply {bal, supply +1 , timestamp}
# tx {bal + 1, supply +1, timestamp}
# tx
# dummy tx ( == last tx in list with time.time() timestamp )


# for each tx 
# IGT += myFunc( tx1, tx2 ) # returns period IGT earned

# # assume 1 mil / month IGT drops 
# # calculate IGT / second 
# # function should return total IGT "Owed"
# # validation in the end should sum all IGT drops and equal IGT / second for seconds since 1st mint

# # add a function variant where user inputs wallet address and IGT is calculated for this user only 