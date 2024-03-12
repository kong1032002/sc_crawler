import requests
import json
from constant import *

def send_request(query):
  response = requests.post(uniswap_api_url, json={'query': query})
  if response.status_code == 200:
      return response.json()
  else:
      raise Exception('Uniswap query failed. return code is {}.{}'.format(response.status_code, query))

def get_pair(smart_contract_addr = '', pair_id=''):
  smart_contract_addr = smart_contract_addr.strip()
  pair_id = pair_id.strip()
  if(smart_contract_addr != ''):
    addrs_str = f'''["{smart_contract_addr}", "{weth_addr}"]'''
    response = send_request(pair_by_token_id % (addrs_str, addrs_str))
  else:
    response = send_request(pair_by_id % pair_id)
  pairs = response['data']['pairs']
  if(len(pairs) == 0):
    raise Exception('Not found pairs between {} and weth'.format(smart_contract_addr))
  pair = pairs[0]
  pair['token'] = pair['token1'] if pair['token0']['symbol'] == 'WETH' else pair['token1']
  return pair

def mint_transaction(pair_address, timestamp_gt = 0):
  try:
    response = send_request(query=mint_query_template % (pair_address, timestamp_gt))
    return response['data']['mints']
  except Exception as e:
    raise Exception('Error in uniswap_grapql.mint_transaction'.format(e))
    
def swap_transaction(pair_address, timestamp_gt = 0):
  try:
    response = send_request(query=swap_query_template % (pair_address, timestamp_gt))
    return response['data']['swaps']
  except Exception as e:
    raise Exception('Error in uniswap_grapql.mint_transaction'.format(e))

def burn_transaction(pair_address, timestamp_gt):
  try:    
    response = send_request(query=burn_query_template % (pair_address, timestamp_gt))
    return response['data']['burns']
  except Exception as e:
    raise Exception('Error in uniswap_grapql.mint_transaction'.format(e))