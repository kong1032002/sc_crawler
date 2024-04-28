import requests
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

def pair_transactions(pair_address, timestamp_gt):
    query_params = f'''
      orderBy: timestamp
      orderDirection: asc
      first: 1000
      where: {{ pair: "{pair_address}", timestamp_gt: {timestamp_gt} }}
    '''
    
    pair_transaction_template = f'''{{
        mints({query_params}) {{
            amount0
            amount1
            to
            sender
            timestamp
            liquidity
            pair {{
                token0 {{ symbol }}
                token1 {{ symbol }}
            }}
        }}
        burns({query_params}) {{
            amount0
            amount1
            to
            liquidity
            amountUSD
            sender
            timestamp
        }}
        swaps({query_params}) {{
            amount0In
            amount0Out
            amount1In
            amount1Out
            to
            sender
            timestamp
            amountUSD
            pair {{
                token0 {{ symbol }}
                token1 {{ symbol }}
            }}
        }}
    }}
    '''
    try:
        response = send_request(pair_transaction_template)
        mints = response['data']['mints']
        burns = response['data']['burns']
        swaps = response['data']['swaps']
        return (mints, burns, swaps)
    except Exception as e:
        raise Exception('Error in uniswap_grapql.pair_transactions'.format(e))