START = "Hello {}, Welcome to COINon price tracker bot"

INVALID_COIN = "Sorry, invalid COIN SYMBOL\n" \
               "(or the coin is not found)\n" \
               "Try again with another one"
OOPS = "Oops, I ran into some problem, please try again😊"

FULL_INFO = "Name      : {0:<5}\n" \
            "Price USD : ${1:<5}\n" \
            "ATH       : ${2:<5}\n" \
            "ATL       : ${3:<5}\n" \
            "High 24-h : ${4:<5}\n" \
            "Low 24-h  : ${5:<5}\n" \
            "_________________________\n" \
            "Price change\n" \
            "1-h  : {6:<10} %  {7:<5}\n" \
            "24-h : {8:<10} %  {9:<5}\n" \
            "7-d  : {10:<10} %  {11:<5}\n" \
            "14-d : {12:<10} %  {13:<5}\n" \
            "30-d : {14:<10} %  {15:<5}\n"

COIN_DETAILED = "Name      :  {0:<5}\n" \
                "Price USD : ${1:<5}\n" \
                "ATH       : ${2:<5}\n" \
                "ATL       : ${3:<5}\n" \
                "High 24-h : ${4:<5}\n" \
                "Low 24-h  : ${5:<5}\n" \
                "_________________________\n" \
                "Price change\n" \
                "1-h  : {6:<10} %  {7:<1}\n" \
                "24-h : {8:<10} %  {9:<1}\n" \
                "7-d  : {10:<10} %  {11:<1}\n" \
                "14-d : {12:<10} %  {13:<1}\n" \
                "30-d : {14:<10} %  {15:<1}\n" \
                "_________________________\n" \
                "Market Cap\n" \
                "Rank       :  {16:<5}\n" \
                "Market Cap :  {17:<5}\n" \
                "Change 24 h\n" \
                "USD : ${18:<9}    {19:<1}\n" \
                "%   :  {20:<9} %  {21:<1}\n" \
                "_________________________\n" \
                "24 H Trading Vol  : ${22:<5}\n" \
                "Total Supply      :  {23:<5}\n" \
                "Maximum Supply    :  {24:<5}\n" \
                "Circulating Supply:  {25:<5}\n"

WAIT = '⏱️ Please Wait\n\n' \
       '📊 Getting data\n\n' \
       '🤑 It may take some time\n\n' \
       '😀 Made by @binarystack 😀'

BITPRICE = '🚀\nPrice USD  : ${0:0.8f}\n\n' \
           '🚀\nPrice {1:<1} : {2:0.8f} {3:<1}'

PAIRADDRESS = "[{}]({})"

WEB3PRICE = '🚀\nPrice {0}  : ${1:0.8f}\n\n'

WEBSITE = ''
COINGECKO = ''
POOCOIN = ''
BOGGED = ''
PANCAKESWAP = ''
BSCSCAN = ''
GITHUB = ''

DEVELOPERURL = ''

PRICETEXT = f'[🌐 Website]({WEBSITE}) | [🦎 CoinGecko]({COINGECKO})\n\n' \
            f'📈 *Chart*  [💩 PooCoin]({POOCOIN}) |  [💹 Bogged]({BOGGED})\n\n' \
            f'💫 *Buy*  [🥞 PancakeswapV2]({PANCAKESWAP})\n\n' \
            f'[🔍 BSC scan]({BSCSCAN}) | [🤖 Github]({GITHUB})\n\n' \
            f'__________________________\n' \
            f'[🤖 Contact Bot developer 🤖]({DEVELOPERURL})'.replace('_','\_')
