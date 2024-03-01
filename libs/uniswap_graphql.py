import requests

api_url = "https://api.thegraph.com/subgraphs/name/ianlapham/uniswap-v2-dev"

pairs_query_template_0 = '''
{
    pairs(first: 100, orderBy: createdAtBlockNumber, orderDirection: desc, where: { token0_contains: "%s" }) 
    {
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
  }
}
'''

pairs_query_template_1 = '''
  {
  pairs(first: 100, orderBy: createdAtBlockNumber, orderDirection: desc, where:{ token1_contains: "%s"}) {
    id
    token0{
      id
      symbol
      name
      txCount
      totalLiquidity
      decimals
    }
    token1{
      id
      symbol
      name
      txCount
      totalLiquidity
      decimals
    }
    reserve0
    reserve1
    totalSupply
    reserveUSD
    reserveETH
    txCount
    createdAtTimestamp
    createdAtBlockNumber
  }
  }
'''

mint_query_template = '''
{
  mints(first: 1000, orderBy: timestamp, orderDirection: asc, where:{ pair: "%s" , timestamp_gt:%s  }) {
      amount0
      amount1
      to
      sender
      timestamp
 }
}
''' 

swap_query_template = '''
{
  swaps(first: 1000, orderBy: timestamp, orderDirection: asc, where:{ pair: "%s" , timestamp_gt:%s }) {
      amount0In
      amount0Out
      amount1In
      amount1Out
      to
      sender
      timestamp
 }
}
''' 

burn_query_template = '''
{
  burns(first: 1000, orderBy: timestamp, orderDirection: asc, where:{ pair: "%s" , timestamp_gt:%s }) {
      amount0
      
      amount1
      to
      sender
      timestamp
 }
}
''' 

def send_request(query):
    # endpoint where you are making the request
    response = requests.post(api_url, json={'query': query})
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception('Query failed. return code is {}.{}'.format(response.status_code, query))

def get_pair(addr): 
    response_1 = send_request(pairs_query_template_0 % addr)
    response_2 = send_request(pairs_query_template_1 % addr)
    result = response_1['data']['pairs'] + response_2['data']['pairs']
    return result

def mint_transaction(pair_address, timestamp):
    try:
        response = send_request(query=mint_query_template % (pair_address, timestamp))
        return response['data']['mints']
    except Exception as e:
        raise Exception('Error in uniswap_grapql.mint_transaction'.format(e))
    
def swap_transaction(pair_address, timestamp):
    try:
        response = send_request(query=swap_query_template % (pair_address, timestamp))
        return response['data']['swaps']
    except Exception as e:
        raise Exception('Error in uniswap_grapql.mint_transaction'.format(e))

def burn_transaction(pair_address, timestamp):
    try:    
        response = send_request(query=burn_query_template % (pair_address, timestamp))
        return response['data']['burns']
    except Exception as e:
        raise Exception('Error in uniswap_grapql.mint_transaction'.format(e))
    
def get_holders(token_id):
    repos_url = 'https://api.ethplorer.io/getTopTokenHolders/'+token_id+'?apiKey=EK-4L18F-Y2jC1b7-9qC3N&limit=100'
    response = requests.get(repos_url)
    if(response.status_code == 400):
        return []
    repos = json.loads(response.text)    #json 형태로 token_id에 해당하는 정보를 불러온다.
    return repos['holders']
