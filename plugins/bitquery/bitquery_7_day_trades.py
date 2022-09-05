from concurrent.futures import process
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath('ABI.py')))
import time
import requests
from datetime import datetime, timedelta
from millify import millify
import numpy as np
from Constants.ADDRESS import address_COIN, address_WETH

from dotenv import load_dotenv
load_dotenv()

bitquery_api_key = os.getenv('BITQUERY_API_KEY')
bot_data_ = {"lastVolCall": 0, "lastVolData": 0}

# print(utc_time_now, utc_time_24hrs_ago)
# The GraphQL query
query = """query ($utc_before: ISO8601DateTime, $utc_now: ISO8601DateTime, $contract_coin:String, $contract_weth:String) {
  seven_days: ethereum(network: ethereum) {
    dexTrades(
      options: {asc: "timeInterval.day"}
      baseCurrency: {is: $contract_coin}
      quoteCurrency: {is: $contract_weth}
      time: {since: $utc_before, before: $utc_now}
    ){
      timeInterval{
        day
      }
      trades: count
      buyAmount(in: USD)
      sellAmount(in: USD)
    }
  }
}"""

def run_query(query):
    try:
        headers = {'X-API-KEY': bitquery_api_key}

        utc_time_now = datetime.utcnow()
        utc_time_7days_ago = utc_time_now - timedelta(days=7)
        utc_time_now = utc_time_now.strftime("%Y-%m-%dT%H:%M:%SZ")
        utc_time_7days_ago = utc_time_7days_ago.strftime("%Y-%m-%dT00:00:00Z")

        variables = {'utc_now': utc_time_now,
                     'utc_before': utc_time_7days_ago, 
                     'contract_coin': address_COIN,
                     'contract_weth': address_WETH}
        request = requests.post('https://graphql.bitquery.io/', json={'query': query, 'variables': variables}, headers=headers)
        if request.status_code == 200:
            return request.json()
        else:
            raise Exception('Query failed and return code is {}.      {}'.format(request.status_code, query))
    except Exception as e:
        print(f"bitquery error , {e}")
        return ''

def getVolume():
    timeout = 300
    try:
        lastVolCall = bot_data_['lastVolCall']
    except:
        lastVolCall = None
    try:
        lastVolData = bot_data_["lastVolData"]
    except:
        lastVolData = None

    if lastVolCall and lastVolData:
        timediff = time.time() - lastVolCall
        if timediff > timeout:
            runVol = True
        else:
            runVol = False
    else:
        runVol = True

    if runVol:
        bot_data_['lastVolCall'] = time.time()
        print("new Vol data fetched")
        resp = run_query(query)
        data = ''
        try:
            data = resp['data']['seven_days']['dexTrades']
        except Exception as e:
            print(f'getVolError: {e}')

        if data:
            tradeText = ''
            for single_data in data:
                try:
                    day = single_data['timeInterval']['day']
                    trades = single_data['trades']
                    tradeAmtUSD = single_data['tradeAmount']
                    try:
                        trades = millify(trades)
                        tradeAmtUSD = millify(tradeAmtUSD, precision=2)
                    except:
                        pass
                    tradeText = f"{tradeText}" \
                                f"________________________\n" \
                                f"📅 {day}\n" \
                                f"💡 Total Tx: {trades}\n" \
                                f"🌳 Tx Vol  : ${tradeAmtUSD}\n"
                    bot_data_["lastVolData"] = tradeText
                except Exception as e:
                    print(e)

            try:
                return tradeText
            except Exception as e:
                print(e)
                return ''
        return ''
    else:
        print("cached Vol data fetched")
        try:
            return bot_data_["lastVolData"]
        except:
            return ''

def process_json():
    timeout = 300
    try:
        lastVolCall = bot_data_['lastVolCall']
    except:
        lastVolCall = None
    try:
        lastVolData = bot_data_["lastVolData"]
    except:
        lastVolData = None

    if lastVolCall and lastVolData:
        timediff = time.time() - lastVolCall
        if timediff > timeout:
            runVol = True
        else:
            runVol = False
    else:
        runVol = True

    if runVol:
        bot_data_['lastVolCall'] = time.time()
        print("new Vol data fetched")
        try:
            data = run_query(query)
            data = data['data']['seven_days']['dexTrades']
        except Exception as e:
            print(f'getVolError: {e}')
            data = ''

        day_array = []
        tx_number_array = []
        buy_amount_array = []
        sell_amount_array = []
        tx_amount_array = []

        if data:
            # tradeText = ''
            for single_data in data:
                try:
                    day = single_data['timeInterval']['day']
                    trades = single_data['trades']
                    buyAmtUSD = single_data['buyAmount']
                    sellAmtUSD = single_data['sellAmount']
                    tradeAmtUSD = buyAmtUSD + sellAmtUSD

                    day_array.append(day)
                    tx_number_array.append(trades)
                    buy_amount_array.append(buyAmtUSD)
                    sell_amount_array.append(sellAmtUSD)
                    tx_amount_array.append(tradeAmtUSD)
                    # try:
                    #     trades2 = millify(trades)
                    #     tradeAmtUSD2 = millify(tradeAmtUSD, precision=2)
                    #     tradeText = f"{tradeText}" \
                    #                 f"________________________\n" \
                    #                 f"📅 {day}\n" \
                    #                 f"💡 Total Tx: {trades2}\n" \
                    #                 f"🌳 Tx Vol  : ${tradeAmtUSD2}\n"
                    # except:
                    #     pass

                except Exception as e:
                    print(e)

            # print(tradeText)
            try:
                day_array = np.array(day_array)
                tx_number_array = np.array(tx_number_array)
                tx_amount_array = np.array(tx_amount_array)
                return_data = {'day_array': day_array,
                               'tx_number_array': tx_number_array,
                               'buy_amount_array': buy_amount_array,
                               'sell_amount_array': sell_amount_array,
                               'tx_amount_array': tx_amount_array,
                               }
                bot_data_["lastVolData"] = return_data
                return return_data
            except Exception as e:
                print(e)
                return ''
        return ''
    else:
        print("cached Vol data fetched")
        try:
            return bot_data_["lastVolData"]
        except:
            return ''
