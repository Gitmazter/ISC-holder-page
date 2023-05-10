from modules.supply.supply_helpers import add_ignored_wallets_events, add_burn_events
from services.solscan_getters import callMetaApi, query_mint_authority

def update_coin_supply(supply_collection, all_holders_collection):
    print("checking and updating total supply...")

    coin_meta_data = callMetaApi()
    metaSupply = coin_meta_data['supply']; 
    
    mint_event_array = query_mint_authority();
    mints_and_ignored_wallet_event_array = add_ignored_wallets_events(mint_event_array, all_holders_collection)
    mints_and_ignored_wallets_and_burns_event_array = add_burn_events(mints_and_ignored_wallet_event_array, all_holders_collection)

    supply_events_cursor_object = supply_collection.find({})
    db_supply_events_array = []
    for supply_event_in_cursor_object in supply_events_cursor_object:
        db_supply_events_array.append(supply_event_in_cursor_object)

    fetchSupply = 0;
    for mint in mints_and_ignored_wallets_and_burns_event_array:
        fetchSupply += float(mint["amount"])

    print("before: " +str(fetchSupply) + "  Now: " + metaSupply) ##  THERE IS BURN!!

    for event in mints_and_ignored_wallets_and_burns_event_array:
        new_event = True
        for db_mint in db_supply_events_array:
            if event["_id"] == db_mint["_id"]:
                new_event = False
        if new_event == True:
            print("found new event! Adding to list....")
            supply_collection.insert_one(event)

    print("total supply updated successfully!")
    return metaSupply

def update_circulating_supply(all_holders_collection, supply_collection):
    totalSupply = update_coin_supply(supply_collection, all_holders_collection);
    print("checking and updating circulating supply...")

    fetched_holders = all_holders_collection.find({})
    holders = []
    for fetched_holder in fetched_holders:
        holders.append(fetched_holder)

    ## Get Ignored Wallets balances
    ignoredAmount = 0.00

    for holder in holders:
        if (holder["ignored"] == True):
            ignoredAmount += holder["amount"]

    circulatingSupply = float(totalSupply) - ignoredAmount

    print("Total Supply:  " + str(totalSupply))
    print("Uncirculating Supply:  " + str(ignoredAmount))
    print("Circulating Supply:  " + str(circulatingSupply))

    print("circulating supply updated successfully!")
    return circulatingSupply