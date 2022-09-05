from asyncio import constants
import json
from web3 import Web3
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath('ABI.py')))
from Constants import ABI
from Constants import ADDRESS
from millify import millify, prettify
from dotenv import load_dotenv

load_dotenv()


all_endpoints = [os.getenv('ALCHEMY_API_URL'),
                 'https://main-light.eth.linkpool.io/',
                 'https://main-light.eth.linkpool.io/',
                 'https://main-light.eth.linkpool.io/',
                 'https://nodes.mewapi.io/rpc/eth',
                 'https://nodes.mewapi.io/rpc/eth',
                 'https://nodes.mewapi.io/rpc/eth',
                 'https://api.mycryptoapi.com/eth',
                 'https://api.mycryptoapi.com/eth',
                 'https://mainnet-nethermind.blockscout.com/',
                 'https://mainnet-nethermind.blockscout.com/',
                 ]

endpoints_length = len(all_endpoints)

large_number_factor = 1  # in billion =>10**9
lrg = millify(large_number_factor)
prefixes = ['k', 'M', 'B', 'T', 'q']


def get_coin_price():
    for endpoint in all_endpoints:
        try:
            global w3
            w3 = Web3(Web3.HTTPProvider(endpoint))
            data = getPrice2_eth()
            if data:
                return data
            if endpoint == all_endpoints[endpoints_length - 1]:
                return data
        except Exception as e:
            print(f"Connect Error {endpoint} : {e}")

# global token0Symbol, token1Symbol, token0Decimal, token1Decimal, coin_name , coin_decimal


def getPrice2_eth():
    try:
        # get an instance of the contract (wETH-COIN)
        abi_WETH_COIN = json.loads(ABI.abi_WETH_COIN)
        address_WETH_COIN = w3.toChecksumAddress(ADDRESS.address_WETH_COIN)
        contract_WETH_COIN = w3.eth.contract(
            address=address_WETH_COIN, abi=abi_WETH_COIN)

        # get an instance of the contract (WETH-USDC)
        abi_WETH_USDC = json.loads(ABI.abi_WETH_USDC)
        address_WETH_USDC = w3.toChecksumAddress(ADDRESS.address_WETH_USDC)
        contract_ETH_USDC = w3.eth.contract(
            address=address_WETH_USDC, abi=abi_WETH_USDC)

        # get an instance of the contract (COIN)
        abi_COIN = json.loads(ABI.abi_COIN)
        address_COIN = w3.toChecksumAddress(ADDRESS.address_COIN)
        contract_coin = w3.eth.contract(address=address_COIN, abi=abi_COIN)

        # get the token0 symbol, token1 symbol, token0 decimal, token1 decimal
        if ADDRESS.address_COIN.lower() < ADDRESS.address_WETH.lower():
            token0Symbol = contract_coin.functions.symbol().call()
            token1Symbol = 'WETH'
            token0Decimal = contract_coin.functions.decimals().call()
            token1Decimal = 18
            coin_name = token0Symbol
        else:
            token0Symbol = 'WETH'
            token1Symbol = contract_coin.functions.symbol().call()
            token0Decimal = 18
            token1Decimal = contract_coin.functions.decimals().call()
            coin_name = token1Symbol

        # get the reserve of token0 and token1
        reserve_WETH_COIN = contract_WETH_COIN.functions.getReserves().call()

        reserve_token0 = reserve_WETH_COIN[0] / 10 ** token0Decimal
        reserve_token1 = reserve_WETH_COIN[1] / 10 ** token1Decimal

        if token0Symbol == 'WETH':
            coin_name = token1Symbol
            coin_decimal = token1Decimal

            coinPriceWETH = (reserve_token0 / reserve_token1) * \
                large_number_factor
            ETHLiquidity = reserve_token0
            coinLiquidity = reserve_token1
        else:
            coin_name = token0Symbol
            coin_decimal = token0Decimal

            coinPriceWETH = (reserve_token1 / reserve_token0) * \
                large_number_factor
            ETHLiquidity = reserve_token1
            coinLiquidity = reserve_token0

        ETHPriceCoin = (1 / coinPriceWETH) * large_number_factor
    except Exception as e:
        print(f'coinPrice Error 1 :{e}')
        coinPriceWETH = float('NaN')
        ETHPriceCoin = float('NaN')
        ETHLiquidity = float('NaN')

    try:
        reserve_ETH_USDC = contract_ETH_USDC.functions.getReserves().call()
        ETHPriceUSDC = (reserve_ETH_USDC[0] / reserve_ETH_USDC[1]) * 10 ** 12
        coinPriceUSDC = coinPriceWETH * ETHPriceUSDC
    except Exception as e:
        print(f'coinPrice Error 2 :{e}')
        ETHPriceUSDC = float('NaN')
        coinPriceUSDC = float('NaN')

    try:
        totalSupply = contract_coin.functions.totalSupply().call() / 10 ** coin_decimal
        totalBurn = contract_coin.functions.balanceOf(
            w3.toChecksumAddress(ADDRESS.burn_address)).call() / 10 ** coin_decimal
        totalBurnPercent = totalBurn * 100 / totalSupply
        marketCap = (totalSupply - totalBurn) * \
            coinPriceUSDC / large_number_factor
        circulatingSupply = totalSupply - totalBurn
    except Exception as e:
        print(f'coinPrice Error 3 :{e}')
        totalSupply = float('NaN')
        marketCap = float('NaN')
        totalBurn = float('NaN')
        totalBurnPercent = float('NaN')
        circulatingSupply = float('NaN')

    try:
        usdLiquidity = ETHLiquidity * ETHPriceUSDC
    except Exception as e:
        print(f'coinPrice Error 4 :{e}')
        usdLiquidity = float('NaN')

    try:
        usdBurned = totalBurn * coinPriceUSDC / large_number_factor
    except Exception as e:
        print(f'coinPrice Error 5 :{e}')
        usdBurned = float('NaN')

    try:
        marketCap = millify(round(marketCap, 2), precision=3)
        totalSupply = millify(totalSupply, precision=2, prefixes=prefixes)
        circulatingSupply = millify(
            circulatingSupply, precision=2, prefixes=prefixes)
        ETHLiquidity = millify(ETHLiquidity, precision=1)
        usdLiquidity = millify(usdLiquidity, precision=2)
        coinLiquidity = millify(coinLiquidity, precision=2)
        totalBurn = millify(totalBurn, precision=2, prefixes=prefixes)
        usdBurned = millify(usdBurned, precision=2, prefixes=prefixes)
        totalBurnPercent = '{:.2f}'.format(totalBurnPercent)
        coinPriceUSDC = '{:.9f}'.format(coinPriceUSDC)
        coinPriceWETH = '{:.8f}'.format(coinPriceWETH)
        ETHPriceCoin = millify(round(ETHPriceCoin, 2), precision=3)
        ETHPriceUSDC = prettify(round(ETHPriceUSDC, 2))
    except:
        pass

    data = (f"*ETHER*\n\n"
            f"🤑*{lrg} ${coin_name}* = ${coinPriceUSDC} 🤑\n"
            f"🚀*{lrg} ${coin_name}* =  {coinPriceWETH} ETH🚀\n\n"
            f"💎*1 ETH*  = ${ETHPriceUSDC}💎\n"
            f"💠*1 ETH*  =  {ETHPriceCoin} ${coin_name}💠\n\n"
            f"💰*MarketCap*: ${marketCap} 💰\n\n"
            f"💵*Total Supply*: {totalSupply} 💵\n\n"
            f"💸*Circulating Supply*: {circulatingSupply} 💸\n\n"
            f"🔥*Burned*: {totalBurn} | {totalBurnPercent}% | ${usdBurned}🔥\n\n"
            f"💧*Liquidity*: ${usdLiquidity} | {ETHLiquidity} ETH | {coinLiquidity} {coin_name}💧\n\n"
            )
    return data
