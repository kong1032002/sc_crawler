from libs.uniswap_graphql import *
from libs.data_parse import *
from libs.ethplorer import *

def preprocessing(early_predict, smart_contract_addr = '', pair_id = '' ):
    pair = get_pair(smart_contract_addr=smart_contract_addr, pair_id=pair_id)
    info = get_token_info(pair['token']['id'])
    token_creator = info['owner'] if 'owner' in info else ""
    
    lp_holders = get_holders(pair['id'])
    lp_lock_ratio = get_lock_ratio(holders=lp_holders)
    lp_avg,lp_std = calc_lp_distribution(lp_holders)
    lp_creator_holding_ratio = get_creator_ratio(holders=lp_holders, creator_address=token_creator)
    
    mint_data_transaction = mint_transaction(pair_address=pair['id'], timestamp_gt=0)
    swap_data_transaction = swap_transaction(pair_address=pair['id'], timestamp_gt=0)
    burn_data_transaction = burn_transaction(pair_address=pair['id'], timestamp_gt=0)
    
    initial_timestamp = int(mint_data_transaction[0]['timestamp'])
    
    mint_data_transaction = get_first_transaction_period(mint_data_transaction, initial_timestamp, early_predict)
    swap_data_transaction = get_first_transaction_period(swap_data_transaction, initial_timestamp, early_predict)
    burn_data_transaction = get_first_transaction_period(burn_data_transaction, initial_timestamp, early_predict)
    
    mint_count = len(mint_data_transaction)
    swap_count = len(swap_data_transaction)
    burn_count = len(burn_data_transaction)
    
    last_timestamp = get_last_timestamp(mint_data_transaction, swap_data_transaction, burn_data_transaction)
    active_period = last_timestamp - initial_timestamp
    
    mint_mean_period = int(get_mint_mean_period(mint_data_transaction, initial_timestamp))
    swap_mean_period = int(get_swap_mean_period(swap_data_transaction, initial_timestamp))
    burn_mean_period = int(get_burn_mean_period(burn_data_transaction, initial_timestamp))
    
    swap_in,swap_out = swap_io_rate(swap_data_transaction,token_index(pair))
    token_holders = get_holders(pair['token']['id'])
    token_burn_ratio = get_burn_ratio(holders=lp_holders) 
    token_creator_holding_ratio = get_creator_ratio(token_holders,token_creator)
        
    data = {
        'id': pair['id'],
        'Label': None,
        'mint_count_per_week': mint_count / ((int(active_period) / (60* 60 * 24 * 7)) + 1),
        'burn_count_per_week': burn_count / ((int(active_period) / (60* 60 * 24 * 7)) + 1),
        'mint_ratio': mint_count / (mint_count + burn_count + swap_count),
        'swap_ratio': swap_count / (mint_count + burn_count + swap_count),
        'burn_ratio': burn_count / (mint_count + burn_count + swap_count),
        'mint_mean_period': mint_mean_period / active_period,
        'swap_mean_period': swap_mean_period / active_period,
        'burn_mean_period': burn_mean_period / active_period,
        'swap_in_per_week': swap_in /((int(active_period) / (60* 60 * 24 * 7)) + 1),
        'swap_out_per_week': swap_out /((int(active_period) / (60* 60 * 24 * 7)) + 1),
        'swap_rate': swap_in / (swap_out + 1),
        'lp_avg': lp_avg,
        'lp_std': lp_std,
        'lp_creator_holding_ratio': lp_creator_holding_ratio,
        'lp_lock_ratio': lp_lock_ratio,
        'token_burn_ratio': token_burn_ratio,
        'token_creator_holding_ratio': token_creator_holding_ratio,
    }
    print("Get info success full")
    return data