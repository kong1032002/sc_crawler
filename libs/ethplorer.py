import requests
from constant import *
def get_token_info(token_id):
    response = requests.get(token_info_ethplorer_api_url % token_id)
    if(response.status_code == 200):
        return response.json()['tokenInfo']
    else:
      raise Exception('ETH plorer get failed. return code is {}.{}'.format(response.status_code,response.json()))

def get_holders(token_id):
    request_url = holders_ethplorer_api_url % token_id
    response = requests.get(request_url)
    if(response.status_code == 200):
        return response.json()["holders"]
    raise Exception('ETH plorer get failed. return code is {}.\n{}'.format(response.status_code,response.json()))
