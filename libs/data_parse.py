from constant import *
from math import sqrt
import json
import datetime

def get_last_timestamp(mint_data_transaction, swap_data_transaction, burn_data_transaction):
    swap_len = len(swap_data_transaction)
    burn_len = len(burn_data_transaction)
    # Case 1 only mint transaction
    if(swap_len == 0 and burn_len == 0):
        return int(mint_data_transaction[-1]['timestamp'])
    
    # Case 2 mint and burn
    if(swap_len == 0):
        return int(max(mint_data_transaction[-1]['timestamp'],burn_data_transaction[-1]['timestamp']))
        
    # Case 3 mint and swap
    if(burn_len == 0):
        return int(max(mint_data_transaction[-1]['timestamp'],swap_data_transaction[-1]['timestamp']))
    return int(max(mint_data_transaction[-1]['timestamp'],burn_data_transaction[-1]['timestamp'],swap_data_transaction[-1]['timestamp']))

def get_mint_mean_period(mint_data_transaction,initial_timestamp):
    count = len(mint_data_transaction)
    if(count == 0):
      return 0
    mint_time_add = 0
    for transaction in mint_data_transaction:
      mint_time_add = mint_time_add + int(transaction['timestamp']) - initial_timestamp
    return mint_time_add / count

def get_swap_mean_period(swap_data_transaction,initial_timestamp):
    count = len(swap_data_transaction)
    if(count == 0):
      return 0
    swap_time_add = 0
    for transaction in swap_data_transaction:
      swap_time_add = swap_time_add + int(transaction['timestamp']) - initial_timestamp
    return swap_time_add / count

def get_burn_mean_period(burn_data_transaction,initial_timestamp):
    count = len(burn_data_transaction)
    if(count == 0):
      return 0
    burn_time_add = 0
    for transaction in burn_data_transaction:
      burn_time_add = burn_time_add + int(transaction['timestamp']) - initial_timestamp
    return burn_time_add / count

def swap_io_rate(swap_data_transaction,index):
    swapIn = 0
    swapOut = 0
    if(index == 1):
        for data in swap_data_transaction:
            if(data['amount0In'] == '0'):
                swapOut = swapOut + 1
            else:   
                swapIn = swapIn + 1
    else:         #amount1이 이더
        for data in swap_data_transaction:
            if(data['amount1In'] == '0'):
                swapOut = swapOut + 1
            else:
                swapIn = swapIn +1
    return swapIn,swapOut 

def get_burn_ratio(holders):
    for holder in holders:
        if(holder['address'] in burn_address):
            return holder['share']
    return 0

def get_creator_ratio(holders,creator_address):
    for holder in holders:
        if(holder['address'] == creator_address):
            return holder['share']
    return 0

def get_lock_ratio(holders):
    for holder in holders:
        if(holder['address'] in locker_address):
          return holder['share']
    return 0

def calc_lp_distribution(holders):
    count = 0
    for holder in holders:
        if(holder['share'] < 0.01 ):
            break
        count = count + 1
    LP_avg = 100 / count
    var = 0
    for i in range(count):
        var = var + (holders[i]['share'] - LP_avg) ** 2
    LP_stdev = sqrt(var)
    return LP_avg,LP_stdev

def token_index(pair):
  if(pair['token0']['symbol'] == 'WETH'):
    return 1
  else:
    return 0

def get_first_transaction_period(data_transactions, initial_timestamp, days):
   return [data for data in data_transactions if int(data['timestamp']) < (initial_timestamp + timestamp_to_date * days)]