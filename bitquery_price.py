import asyncio
import httpx
from cred import Creds

# The GraphQL query
query = """
{
  ethereum(network: bsc) {
    dexTrades(
      options: {desc: ["block.height","tradeIndex"], limit: 1}
      exchangeName: {in: ["Pancake", "Pancake v2"]}
      baseCurrency: {is: "0x6c1de9907263f0c12261d88b65ca18f31163f29d"}
      date: {after: "2021-04-28"}
    ) {
      transaction {
        hash
      }
      tradeIndex
      smartContract {
        address {
          address
        }
        contractType
        currency {
          name
        }
      }
      tradeIndex
      date {
        date
      }
      block {
        height
      }
      buyAmount
      buyAmountInUsd: buyAmount(in: USD)
      buyCurrency {
        symbol
        address
      }
      sellAmount
      sellAmountInUsd: sellAmount(in: USD)
      sellCurrency {
        symbol
        address
      }
      tradeAmount(in: USD)
      transaction {
        gasValue
        gasPrice
        gas
      }
    }
  }
}
"""


async def run_query():
    headers = {'X-API-KEY': Creds.bitquery_api_key}
    async with httpx.AsyncClient() as client:
        resp = await client.post('https://graphql.bitquery.io/',
                                 json={'query': query},
                                 headers=headers)
        if resp.status_code is not httpx.codes.OK.value:
            raise Exception('Query failed and return code is {}.      {}'.format(resp.status_code, query))
        return resp.json()