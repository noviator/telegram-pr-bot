import json
from web3 import Web3
from plugins import abi_all
from plugins.address_all import address
from millify import millify, prettify
from cred import Creds

from pycoingecko import CoinGeckoAPI

# HTTPProvider:
try:
    w3 = Web3(Web3.HTTPProvider(f'https://bsc-mainnet.web3api.com/v1/{Creds.web3_api_key}'))
except Exception as e:
    print(f"Connect Error : {e}")


def getCirSupply():
    cg = CoinGeckoAPI()
    circulating_supply = cg.get_coin_by_id(id='COINName')["market_data"]["circulating_supply"]
    return circulating_supply

def getPrice():
    try:
        abi_WBNB_COIN = json.loads(abi_all.abi_WBNB_COIN)
        address_WBNB_COIN = w3.toChecksumAddress(address.address_WBNB_COIN)

        contract_WBNB_COIN = w3.eth.contract(address=address_WBNB_COIN, abi=abi_WBNB_COIN)
        reserve_WBNB_COIN = contract_WBNB_COIN.functions.getReserves().call()
        coinPriceWBNB = reserve_WBNB_COIN[1] / reserve_WBNB_COIN[0]
        bnbPriceCoin = 1 / coinPriceWBNB
        bnbLiquidity = float(w3.fromWei(reserve_WBNB_COIN[1], 'ether'))
    except Exception as e:
        print(f'coinPrice Error 1 :{e}')
        coinPriceWBNB = float('NaN')
        bnbPriceCoin = float('NaN')
        bnbLiquidity = float('NaN')

    try:
        abi_BNB_BUSD = json.loads(abi_all.abi_BNB_BUSD)
        address_BNB_BUSD = w3.toChecksumAddress(address.address_BNB_BUSD)

        contract_BNB_BUSD = w3.eth.contract(address=address_BNB_BUSD, abi=abi_BNB_BUSD)
        reserve_BNB_BUSD = contract_BNB_BUSD.functions.getReserves().call()
        bnbPriceBUSD = reserve_BNB_BUSD[1] / reserve_BNB_BUSD[0]
        coinPriceBUSD = coinPriceWBNB * bnbPriceBUSD
    except Exception as e:
        print(f'coinPrice Error 2 :{e}')
        bnbPriceBUSD = float('NaN')
        coinPriceBUSD = float('NaN')

    try:
        abi_coin = json.loads(abi_all.abi_coin)
        address_coin = w3.toChecksumAddress(address.address_coin)

        contract_coin = w3.eth.contract(address=address_coin, abi=abi_coin)
        totalSupply = float(w3.fromWei(contract_coin.functions.totalSupply().call(), 'ether'))
        # totalBurn = contract_coin.functions.balanceOf(w3.toChecksumAddress(address.burn_address)).call()
        # totalBurnPercent = totalBurn * 100 / (totalSupply)
        # marketCap = (totalSupply) * coinPriceBUSD
    except Exception as e:
        print(f'coinPrice Error 3 :{e}')
        totalSupply = float('NaN')
        # totalBurn = float('NaN')
        # totalBurnPercent = float('NaN')
        # marketCap = float('NaN')

    try:
        usdLiquidity = bnbLiquidity * bnbPriceBUSD
    except Exception as e:
        print(f'coinPrice Error 4 :{e}')
        usdLiquidity = float('NaN')

    try:
        circulating_supply = getCirSupply()
        marketCap = circulating_supply*coinPriceBUSD
    except Exception as e:
        print(f'coinPrice Error 5 :{e}')
        circulating_supply = float('NaN')
        marketCap = float('NaN')



    try:
        marketCap = millify(round(marketCap, 2), precision=3)
    except:
        pass
    try:
        circulating_supply = millify(circulating_supply,precision=2)
    except:
        pass


    try:
        totalSupply = millify(totalSupply, precision=2)
    except:
        pass
    try:
        bnbLiquidity = millify(bnbLiquidity, precision=1)
        usdLiquidity = millify(usdLiquidity, precision=2)
    except:
        pass
    # try:
    #     totalBurn = millify(totalBurn, precision=2)
    # except:
    #     pass
    # try:
    #     totalBurnPercent = '{:.2f}'.format(totalBurnPercent)
    # except:
    #     pass
    try:
        coinPriceBUSD = '{:.9f}'.format(coinPriceBUSD)
    except:
        pass
    try:
        coinPriceWBNB = '{:.9f}'.format(coinPriceWBNB)
        bnbPriceCoin = millify(round(bnbPriceCoin, 2), precision=3)
    except:
        pass
    try:
        bnbPriceBUSD = prettify(round(bnbPriceBUSD, 2))
    except:
        pass

    textPart2 = (
        f"💰*MarketCap*: $*{marketCap}* 💰\n\n"
        f"💵*Total Supply*: {totalSupply} 💵\n\n"
        f"⚜*Circulating Supply*: {circulating_supply} ⚜️\n\n"
        f"💧*Liquidity*: ${usdLiquidity} | {bnbLiquidity} BNB 💧\n\n")


    # f"🔥*Burned*: {totalBurn} | {totalBurnPercent}% 🔥\n\n")

    textPart1 = (f"🤑*1 $COIN* = $*{coinPriceBUSD}* 🤑\n"
                 f"🚀*1 $COIN* =  *{coinPriceWBNB}* BNB🚀\n\n"
                 f"💎*1 BNB*  = ${bnbPriceBUSD}💎\n"
                 f"💠*1 BNB*  =  {bnbPriceCoin} $COIN💠\n\n"
                 )

    return textPart1, textPart2
