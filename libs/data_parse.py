from constant import *
from math import sqrt

def get_last_transaction(mint_data_transaction, swap_data_transaction, burn_data_transaction):
   # Đếm số lượng giao dịch mint, swap và burn
   mint_len, swap_len, burn_len = len(mint_data_transaction), len(swap_data_transaction), len(burn_data_transaction)

   # Lấy thời điểm cuối cùng của mỗi loại giao dịch
   mint_timestamp = int(mint_data_transaction[-1]['timestamp']) if mint_len > 0 else float('-inf')
   swap_timestamp = int(swap_data_transaction[-1]['timestamp']) if swap_len > 0 else float('-inf')
   burn_timestamp = int(burn_data_transaction[-1]['timestamp']) if burn_len > 0 else float('-inf')

   # Tìm thời điểm cuối cùng và trả về giao dịch tương ứng
   last_timestamp = max(mint_timestamp, swap_timestamp, burn_timestamp)
   if last_timestamp == mint_timestamp and mint_len > 0:
      return mint_data_transaction[-1]
   elif last_timestamp == swap_timestamp and swap_len > 0:
      return swap_data_transaction[-1]
   else:
      return burn_data_transaction[-1]

def get_last_timestamp(mint_data_transaction, swap_data_transaction, burn_data_transaction) -> int:
   last_transaction = get_last_transaction(mint_data_transaction, swap_data_transaction, burn_data_transaction)
   return int(last_transaction['timestamp'])

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
   else:
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
   LP_avg = 100 / count if count != 0  else 0
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

def get_price_fluctuation(mint_transactions, swap_transactions, burn_transactions):
   init_price = mint_transactions[0]['amountUSD'] / mint_transactions[0]['liquidity']
   last_transaction = get_last_transaction(mint_transactions, swap_transactions, burn_transactions)
   if last_transaction['liquidity'] != None:
      last_price = int(last_transaction['amountUSD']) / int(last_transaction['liquidity'])
   return 1