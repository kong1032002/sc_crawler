uniswap_api_url = "https://api.thegraph.com/subgraphs/name/ianlapham/uniswap-v2-dev"

token_info_ethplorer_api_url = '''https://api.ethplorer.io/getAddressInfo/%s?apiKey=EK-4L18F-Y2jC1b7-9qC3N'''

holders_ethplorer_api_url = '''https://api.ethplorer.io/getTopTokenHolders/%s?apiKey=EK-4L18F-Y2jC1b7-9qC3N'''

weth_addr = "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"

timestamp_to_date = 86400

burn_address = [
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

proxy_contracts = [
'0x5e5a7b76462e4bdf83aa98795644281bdba80b88',
'0x000000000092c287eb63e8c2c30b4a74787054f8',
'0x0f4676178b5c53ae0a655f1b19a96387e4b8b5f2',
'0xdf65f4e6f2e9436bc1de1e00661c7108290e8bd3',
'0xdb73dde1867843fdca5244258f2fd4b6dc7b154e',
'0xbdb1127bd15e76d7e4d3bc4f6c7801aa493e03f0',
'0x8f84c1d37fa5e21c81a5bf4d3d5f2e718a2d8eb4',
'0x908521c8e53e9bb3b8b9df51e2c6dd3079549382',
'0x85aa7f78bdb2de8f3e0c0010d99ad5853ffcfc63',
'0x909d05f384d0663ed4be59863815ab43b4f347ec',
'0xb4a2810e9d0f1d4d2c0454789be80aaeb9188480',
'0x96fc64f7fe4924546b9204fe22707e3df04be4c8',
'0x226e390751a2e22449d611bac83bd267f2a2caff'
]

locker_address = [
'0x663a5c229c09b049e36dcc11a9b0d4a8eb9db214',
'0xe2fe530c047f2d85298b07d9333c05737f1435fb',
'0x000000000000000000000000000000000000dead' ]

pair_by_id = '''
{
  pairs( where: { 
    id: "%s",
  }) {
    token0 {
      id
      symbol
      txCount
    }
    token1 {
      id
      symbol
      txCount
    }
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

pair_by_token_id = '''
{
  pairs(where: { 
    token0_in: %s,
    token1_in: %s
  }) {
    token0 {
      id
      symbol
      txCount
    }
    token1 {
      id
      symbol
      txCount
    }
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

mint_query_template = '''
{
  mints (
    orderBy: timestamp, 
    orderDirection: asc, 
    first: 1000,
    where: { pair: "%s", timestamp_gt:%s }
  ) {
    amount0
    amount1
    to
    sender
    timestamp
    pair {
      token0 {
        symbol
      }
      token1 {
        symbol
      }
    }
  }
}
''' 

swap_query_template = '''
{
  swaps(
    orderBy: timestamp, 
    orderDirection: asc, 
    first: 1000,
    where:{ pair: "%s" , timestamp_gt:%s }) {
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
  burns(
    orderBy: timestamp, 
    orderDirection: asc, 
    first: 1000
    where: { pair: "%s" , timestamp_gt:%s }) {
    amount0
    amount1
    to
    sender
    timestamp
 }
}
''' 