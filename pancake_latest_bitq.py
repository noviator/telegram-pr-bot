import requests
from plugins import TEXT
from cred import Creds


def run_query(limit):
    query = """{
      ethereum(network: bsc) {
        arguments(smartContractAddress: 
          {in: ["0xBCfCcbde45cE874adCB698cC183deBcF17952812",
          "0xcA143Ce32Fe78f1f7019d7d551a6402fC5350c73"]}, 
          smartContractEvent: {is:"PairCreated"},
          argument: {is:"pair"}
          options: {desc: "block.height", limit: %s}) {
          block {
            height
          }
          argument {
            name
          }
          reference {
            address
          }
        }
      }
    }""" % limit
    headers = {'X-API-KEY': Creds.bitquery_api_key}
    resp = requests.post('https://graphql.bitquery.io/',
                         json={'query': query},
                         headers=headers)
    if resp.status_code == 200:
        return resp.json()
    return None

# response = run_query(10)
# response = response['data']['ethereum']['arguments']
# text = ""
# if response:
#     for data in response:
#         addr = data['reference']['address']
#         link = "https://bscscan.com/address/" + addr
#         text += TEXT.PAIRADDRESS.format(addr, link) + "\n"
#     print(text)


# async def run_query():
#     headers = {'X-API-KEY': Creds.bitquery_api_key}
#     async with httpx.AsyncClient() as client:
#         resp = await client.post('https://graphql.bitquery.io/',
#                                  json={'query': query},
#                                  headers=headers)
#         if resp.status_code is not httpx.codes.OK.value:
#             print('Query failed and return code is {}.      {}'.format(resp.status_code, query))
#             # raise Exception('Query failed and return code is {}.      {}'.format(resp.status_code, query))
#             return None
#         return resp.json()
# response = asyncio.run(run_query())
#
# response = response['data']['ethereum']['arguments']
# if response:
#     for data in response:
#         print("https://bscscan.com/address/" + data['reference']['address'])
