import requests
import json

uniswap_api_url = "https://api.thegraph.com/subgraphs/name/ianlapham/uniswap-v2-dev"

pair_address = "0x81b6c265450273affbbdf35ff38ffc057f414a08"
timestamp_gt = 0

common_query_params = f'''
    orderBy: timestamp
    orderDirection: asc
    first: 1000
    where: {{ pair: "{pair_address}", timestamp_gt: {timestamp_gt} }}
'''

def send_request(query):
    response = requests.post(uniswap_api_url, json={'query': query})
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception('Uniswap query failed. return code is {}.{}'.format(response.status_code, query))

def pair_info_by_id(id):
    query_template = f'''
    {{
        pair(id: "{id}") 
        {{
            token0 {{ symbol }}
            token1 {{ symbol }}
            id
            reserve0
            reserve1
            totalSupply
            reserveETH
            reserveUSD
            trackedReserveETH
            token0Price
            token1Price
            volumeToken0
            volumeToken1
            volumeUSD
            untrackedVolumeUSD
            txCount
            createdAtTimestamp
            createdAtBlockNumber
            liquidityProviderCount
        }}
    }}
    '''
    try:
        return send_request(query_template)
    except Exception as ex:
        raise Exception('Error in uniswap_grapql.pair_transactions'.format(ex))

def pair_info_by_token(tokenId):
    query_template = f'''
    {{
    pairs(where: {{ 
        token0_in: %s,
        token1_in: %s
    }}) {{
        token0 {{ symbol }}
        token1 {{ symbol }}
        id
        reserve0
        reserve1
        totalSupply
        reserveETH
        reserveUSD
        trackedReserveETH
        token0Price
        token1Price
        volumeToken0
        volumeToken1
        volumeUSD
        untrackedVolumeUSD
        txCount
        createdAtTimestamp
        createdAtBlockNumber
        liquidityProviderCount
    }}}}
    '''
    try:
        return send_request(query_template)
    except Exception as ex:
        raise Exception('Error in uniswap_grapql.pair_transactions'.format(ex))

def pair_transactions(query_params):
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

data = pair_info_by_id("0x81b6c265450273affbbdf35ff38ffc057f414a08")

print(json.dumps(data, indent=1))