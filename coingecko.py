from pycoingecko import CoinGeckoAPI
from plugins import TEXT
import json
from millify import millify

cg = CoinGeckoAPI()


def find_info_partial(coin_symbol):
    coin_list = cg.get_coins_list()
    coin_search = coin_symbol.lower()
    coin_info = next(
        (coin for coin in coin_list if coin["symbol"] == coin_search), None)
    return coin_info


def find_id(coin_symbol):
    coin_info_partial = find_info_partial(coin_symbol)
    if coin_info_partial:
        return coin_info_partial["id"]
    else:
        return None


def get_coin_info_full(coin_symbol):
    id = find_id(coin_symbol)
    if id:
        coin_info = cg.get_coin_by_id(id=id)
        return coin_info
    else:
        return None


def print_full_info(coinSymbol):
    coinInf = get_coin_info_full(coinSymbol)
    try:
        if coinInf:
            market_data = coinInf["market_data"]
            change1h = market_data["price_change_percentage_1h_in_currency"]["usd"]
            change24h = market_data["price_change_percentage_24h"]
            change7d = market_data["price_change_percentage_7d"]
            change14d = market_data["price_change_percentage_14d"]
            change30d = market_data["price_change_percentage_30d"]
            green = "🟢"
            red = "🔻"
            c1h_sym = emoji(change1h)
            c24h_sym = emoji(change24h)
            c7d_sym = emoji(change7d)
            c14d_sym = emoji(change14d)
            c30d_sym = emoji(change30d)

            return TEXT.FULL_INFO.format(coinInf["name"], market_data["current_price"]["usd"],
                                         market_data["ath"]["usd"], market_data["atl"]["usd"],
                                         market_data["high_24h"]["usd"],
                                         market_data["low_24h"]["usd"], change1h, c1h_sym, change24h,
                                         c24h_sym, change7d, c7d_sym, change14d, c14d_sym, change30d, c30d_sym)
        else:
            return None
    except:
        return None


def emoji(change):
    green = "🟢"
    red = "🔻"
    if change == 0:
        return ""
    return green if change >= 0 else red


def detailed(coinSymbol):
    coinInf = get_coin_info_full(coinSymbol)
    try:
        if coinInf:
            market_data = coinInf["market_data"]

            coin_name = coinInf["name"]

            change1h = market_data["price_change_percentage_1h_in_currency"]["usd"]
            change24h = market_data["price_change_percentage_24h"]
            change7d = market_data["price_change_percentage_7d"]
            change14d = market_data["price_change_percentage_14d"]
            change30d = market_data["price_change_percentage_30d"]

            emoji1h = emoji(change1h)
            emoji24h = emoji(change24h)
            emoji17d = emoji(change7d)
            emoji14d = emoji(change14d)
            emoji30d = emoji(change30d)

            market_cap = millify(market_data["market_cap"]["usd"], precision=3, drop_nulls=False)

            changeMarketCap24h = market_data["market_cap_change_percentage_24h"]
            emojiMC24hpercent = emoji(changeMarketCap24h)
            changeMarketCap24hMillified = millify(changeMarketCap24h, precision=2, drop_nulls=False)

            changeMarketCap24hNum = market_data["market_cap_change_24h"]
            emojiMC24hNum = emoji(changeMarketCap24hNum)
            changeMarketCap24hNumMillified = millify(changeMarketCap24hNum, precision=2, drop_nulls=False)

            marketCapRank = market_data["market_cap_rank"]

            total_supply = millify(market_data["total_supply"], precision=2, drop_nulls=False)
            max_supply = millify(market_data["max_supply"], precision=2, drop_nulls=False)
            circulating_supply = millify(coinInf["market_data"]["circulating_supply"], precision=2, drop_nulls=False)
            total_vol_24h = millify(market_data["total_volume"]["usd"], precision=2, drop_nulls=False)

            priceusd = market_data["current_price"]["usd"]
            athusd = market_data["ath"]["usd"]
            atlusd = market_data["atl"]["usd"]
            high24 = market_data["high_24h"]["usd"]
            low24 = market_data["low_24h"]["usd"]

            message = TEXT.COIN_DETAILED.format(coin_name, priceusd, athusd, atlusd, high24, low24,
                                                change1h, emoji1h, change24h, emoji24h, change7d,
                                                emoji17d, change14d, emoji14d, change30d, emoji30d, marketCapRank,
                                                market_cap,
                                                changeMarketCap24hNumMillified
                                                , emojiMC24hNum, changeMarketCap24hMillified,
                                                emojiMC24hpercent,
                                                total_vol_24h, total_supply, max_supply,
                                                circulating_supply)

            return message
        else:
            return None
    except:
        return None
circulating_supply = cg.get_coin_by_id(id='CoinNameHere')["market_data"]["circulating_supply"]