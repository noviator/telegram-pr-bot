import time
import requests
from datetime import datetime, timedelta
from plugins.address_all import address
from millify import millify
from cred import Creds
import numpy as np

# print(utc_time_now, utc_time_24hrs_ago)

# The GraphQL query
query = """query ($utc_before: ISO8601DateTime, $utc_now: ISO8601DateTime, $contract_coin:String){

  seven_days: ethereum(network: bsc){
    dexTrades(
      options: {asc: "timeInterval.day"}
      baseCurrency: {is: $contract_coin}
      quoteCurrency: {is: "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c"}
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
bitquery_api_key = Creds.bitquery_api_key
address_coin = address.address_coin


def run_query(query):
    try:
        headers = {'X-API-KEY': bitquery_api_key}

        utc_time_now = datetime.utcnow()
        utc_time_7days_ago = utc_time_now - timedelta(days=7)
        utc_time_now = utc_time_now.strftime("%Y-%m-%dT%H:%M:%SZ")
        utc_time_7days_ago = utc_time_7days_ago.strftime("%Y-%m-%dT00:00:00Z")

        variables = {'utc_now': utc_time_now, 'utc_before': utc_time_7days_ago, 'contract_coin': address_coin}
        request = requests.post('https://graphql.bitquery.io/',
                                json={'query': query, 'variables': variables}, headers=headers)
        if request.status_code == 200:
            return request.json()
        else:
            raise Exception('Query failed and return code is {}.      {}'.format(request.status_code, query))
    except Exception as e:
        print(f"bitquery error , {e}")
        return ''


bot_data_ = {"lastVolCall": 0, "lastVolData": 0}


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
        try:
            data = resp['data']['seven_days']['dexTrades']
        except Exception as e:
            print(f'getVolError: {e}')
            data = ''

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