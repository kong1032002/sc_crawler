from libs.uniswap_graphql import *
from libs.data_parse import *
# import pandas as pd

addr = '0x0383eeb899e7fc0f4f696ebfcb5672ad7e0d271c'

data = {}

data['id'] = addr

mint_data_transaction = mint_transaction(addr, 0)
swap_data_transaction = swap_transaction(addr, 0)
burn_data_transaction = burn_transaction(addr, 0)

mint_count = len(mint_data_transaction)
swap_count = len(swap_data_transaction)
burn_count = len(burn_data_transaction)

initial_timestamp = int(mint_transaction[0]['timestamp'])
last_timestamp = get_last_timestamp(mint_data_transaction, swap_data_transaction, burn_data_transaction)
active_period = last_timestamp - initial_timestamp

mint_mean_period = int(get_mint_mean_period(mint_data_transaction,initial_timestamp))
swap_mean_period = int(get_swap_mean_period(swap_data_transaction,initial_timestamp))
burn_mean_period = int(get_burn_mean_period(burn_data_transaction,initial_timestamp))

swap_in,swap_out = swap_IO_rate(swap_data_transaction,token_index(pair))

token_holders = get_holders(pair.token00.id)   
token_burn_ratio = get_burn_ratio(token_holders)
token_creator_holding_ratio = get_creator_ratio(token_holders,token_creator)
if(lp_lock_ratio > 0):  
    unlock_date = get_unlock_date(lp_holders,token_creator)
else:
    unlock_date = 0


# pairs = get_pair(addr=addr)
# print(pairs)
# current_Liquidity_Eth = Decimal(min)
print(mint_data_transaction)

