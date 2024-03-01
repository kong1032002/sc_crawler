Burn_address = [
    '0x0000000000000000000000000000000000000000',
    '0x0000000000000000000000000000000000000001',
    '0x0000000000000000000000000000000000000002',
    '0x0000000000000000000000000000000000000003',
    '0x0000000000000000000000000000000000000004',
    '0x0000000000000000000000000000000000000005',
    '0x0000000000000000000000000000000000000006',
    '0x0000000000000000000000000000000000000007',
    '0x0000000000000000000000000000000000000008',
    '0x0000000000000000000000000000000000000009',
    '0x000000000000000000000000000000000000000a',
    '0x000000000000000000000000000000000000000b',
    '0x000000000000000000000000000000000000000c',
    '0x000000000000000000000000000000000000000d',
    '0x000000000000000000000000000000000000000e',
    '0x000000000000000000000000000000000000000f',
    '0x000000000000000000000000000000000000dead',
    '0x000000000000000000000000000000000000DEAD'
]

def get_last_timestamp(mint_data_transaction, swap_data_transaction, burn_data_transaction):
    swap_len = len(swap_data_transaction)
    burn_len = len(burn_data_transaction)
    #Case 1 Swap / Burn 전부 0 인경우
    if(swap_len == 0 and burn_len == 0):
        return int(mint_data_transaction[-1]['timestamp'])
    #Case 2 Swap_transaction이 0 인경우
    if(swap_len == 0):
        return int(max(mint_data_transaction[-1]['timestamp'],burn_data_transaction[-1]['timestamp']))
    #Case 3 Burn Transaction이 0 인경우
    if(burn_len == 0):
        return int(max(mint_data_transaction[-1]['timestamp'],swap_data_transaction[-1]['timestamp']))
    #Case 4 전부다 있는 경우
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
      swap_time_add = swap_time_add +  int(transaction['timestamp']) - initial_timestamp
    return swap_time_add / count

def get_burn_mean_period(burn_data_transaction,initial_timestamp):
    count = len(burn_data_transaction)
    if(count == 0):
      return 0
    burn_time_add = 0
    for transaction in burn_data_transaction:
      burn_time_add = burn_time_add + int(transaction['timestamp']) - initial_timestamp
    return burn_time_add / count

def swap_IO_rate(swap_data_transaction,index):
    swapIn = 0
    swapOut = 0
    if(index == 1): #amount0이 이더.
        for data in swap_data_transaction:
            if(data['amount0In'] == '0'): #amount0Out이 0이 아니란 말. 
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
        if(holder['address'] in Burn_address):
            return holder['share']
    return 0

def get_creator_ratio(holders,creator_address):
    for holder in holders:
        if(holder['address'] == creator_address):
            return holder['share']
    return 0