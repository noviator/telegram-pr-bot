import logging
import os
import time

from telegram import ParseMode
from telegram.ext import Updater, CommandHandler, Filters
from plugins.price.coin_price import get_coin_price
from Constants import TEXT
from plugins.latestTweets import getTweetsText
from plugins.price.coingecko import simple_stats_coin, detailed_stats_coin
from collections import deque
from plugins.price.price_for_chart import get_coin_price_chart
from plugins.chart.make_price_chart import create_price_graph
from plugins.chart.trade_graph import create_trade_graph
import numpy as np
from datetime import datetime, timezone
from millify import millify
prefixes = ['k', 'M', 'B', 'T', 'q']




PORT = int(os.environ.get('PORT', 5000))
herokuAppUrl = ''

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def replaceText(text):
    text = text.replace('=', '\=').replace('.', '\.').replace('|', '\|').replace('-', '\-')
    return text

def price(update, context):
    print('price called')

    timeout = 45
    runPrice = False
    try:
        prevTime = context.chat_data['startTime']
    except:
        prevTime = None

    if prevTime:
        timediff = time.time() - prevTime
        if timediff > timeout:
            runPrice = True
        else:
            runPrice = False
            update.message.reply_text(reply_to_message_id=update.message.message_id,
                                      text=f"⌛*Timeout enabled {timeout} seconds*\n"
                                           f"Try after {int(timeout - timediff)} seconds",
                                      parse_mode=ParseMode.MARKDOWN_V2)
    else:
        runPrice = True

    if runPrice:
        context.chat_data['startTime'] = time.time()
        wait_msg = update.message.reply_text(reply_to_message_id=update.message.message_id,
                                             text=TEXT.WAIT,
                                             parse_mode=ParseMode.MARKDOWN_V2)
        try:
            text = get_coin_price()

            if text:
                alltext = replaceText(f'{text}{TEXT.PRICETEXT}')
            else:
                alltext = replaceText(f'{TEXT.PRICETEXT}')


            firstMsg = context.bot.edit_message_text(chat_id=update.effective_chat.id,
                                                     message_id=wait_msg.message_id,
                                                     text=alltext,
                                                     parse_mode=ParseMode.MARKDOWN_V2,
                                                     disable_web_page_preview=True)
            context.chat_data['startTime'] = time.time()
        except Exception as e:
            print(f'bot.py Error 1 :{e}')
            context.bot.edit_message_text(chat_id=update.effective_chat.id,
                                          message_id=wait_msg.message_id,
                                          text="Sorry, failed to get data")
            context.chat_data['startTime'] = time.time()

def chart2(update, context):
    print("chart called")

    try:
        update.message.reply_text(reply_to_message_id=update.message.message_id,
                                  text=replaceText(TEXT.CHART),
                                  parse_mode=ParseMode.MARKDOWN_V2, disable_web_page_preview=True)
    except Exception as e:
        print(e)
        pass

def contract(update, context):
    print("contract called")

    try:
        update.message.reply_text(reply_to_message_id=update.message.message_id,
                                  text=replaceText("Here's the contract address\n\n"
                                                   f"ETH\n"
                                                   f"`{TEXT.CONTRACT}`\n\n"
                                                   f"[Etherscan link]({TEXT.ETHERSCAN})\n\n"),
                                  parse_mode=ParseMode.MARKDOWN_V2,
                                  disable_web_page_preview=True
                                  )
    except Exception as e:
        print(e)
        pass

def tweets(update, context):
    print("tweets called")

    try:
        text = f"*Latest Twitter Posts*\n\n"\
                f"{getTweetsText()}"
        update.message.reply_text(reply_to_message_id=update.message.message_id,
                                  text=replaceText(text), parse_mode=ParseMode.MARKDOWN_V2, disable_web_page_preview=True)
    except Exception as e:
        print(e)
        pass

def repeat_tweet(context):

    chatid = os.getenv('CHAT_ID')
    try:
        text = f"*Latest Twitter Posts*\n\n"\
                f"{getTweetsText()}"
        context.bot.send_message(chat_id= chatid, text=replaceText(text), parse_mode=ParseMode.MARKDOWN_V2, disable_web_page_preview=True)
    except Exception as e:
        print(e)
        pass

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def chart(update, context):
    print("chart called")
    timeoutChart = 10
    runChartPrice = False
    try:
        prevTimeChart = context.chat_data['startTimeChart']
    except:
        prevTimeChart = None

    if prevTimeChart:
        timediff = time.time() - prevTimeChart
        if timediff > timeoutChart:
            runChartPrice = True
        else:
            runChartPrice = False
            update.message.reply_text(reply_to_message_id=update.message.message_id,
                                      text=f"⌛*Timeout enabled {timeoutChart} seconds*\n"
                                           f"Try after {int(timeoutChart - timediff)} seconds",
                                      parse_mode=ParseMode.MARKDOWN_V2)
    else:
        runChartPrice = True

    if runChartPrice:
        context.chat_data['startTimeChart'] = time.time()
        wait_msg_chart = update.message.reply_text(reply_to_message_id=update.message.message_id,
                                                   text=TEXT.WAIT,
                                                   parse_mode=ParseMode.MARKDOWN_V2)

        try:
            pic = create_price_graph(np.array(q))
        except Exception as e:
            pic = ''
            print(f"sendGraph error : {e}")

        if pic:
            try:
                alltext = get_coin_price()
                if alltext:
                    textForChart = replaceText(f'{alltext}{TEXT.PRICETEXT}')
                else:
                    textForChart = replaceText(f'{TEXT.PRICETEXT}')
            except Exception as e:
                textForChart = ''
                print(f"Getting price for Chart Error :{e}")

            try:
                context.bot.delete_message(chat_id=update.effective_chat.id,
                                           message_id=wait_msg_chart.message_id)
            except Exception as e:
                print(f"Failed to Delete Wait Msg :{e}")

            try:

                chart_pic_message = context.bot.send_photo(reply_to_message_id=update.message.message_id,
                                                           chat_id=update.effective_chat.id,
                                                           photo=pic, caption=textForChart,
                                                           parse_mode=ParseMode.MARKDOWN_V2
                                                           )
            except Exception as e:
                print("sendGraph error2 : ", e)
        else:
            text = f"Sorry failed to fetch chart"
            try:
                context.bot.edit_message_text(chat_id=update.effective_chat.id,
                                              message_id=wait_msg_chart.message_id,
                                              text=text)
            except Exception as e:
                print("sendGraph error3 : ", e)

no_of_elements = 4320
q = deque()
def repeat_price(context):
    global q
    try:
        dt = datetime.now(timezone.utc)
        utc_time = dt.replace(tzinfo=timezone.utc)
        # utc_timestamp = utc_time.timestamp()
        # utc_time_now = float(utc_timestamp)

        usdP = get_coin_price_chart()
        if usdP:
            t = (utc_time, usdP)
            q.append(t)
        if len(q) == no_of_elements + 1:
            q.popleft()
    except Exception as e:
        print(f"chart repeat error {e}")

def get_info_of_coin(update, context):
    if len(context.args) != 1:
        update.message.reply_text(reply_to_message_id=update.message.message_id,
                                  text=f"Please enter the command correctly\n\n`/p <CoinSymbol>`",
                                  parse_mode=ParseMode.MARKDOWN_V2)
    else:
        data_message = simple_stats_coin(context.args[0])
        if data_message:
            update.message.reply_text(reply_to_message_id=update.message.message_id,
                                      text="`" + data_message + "`",
                                      parse_mode=ParseMode.MARKDOWN_V2)
        else:
            update.message.reply_text(TEXT.INVALID_COIN)

def get_detailed_info_of_coin(update, context):
    if len(context.args) != 1:
        update.message.reply_text(reply_to_message_id=update.message.message_id,
                                  text=f"Please enter the command correctly\n\n`/pc <CoinSymbol>`",
                                  parse_mode=ParseMode.MARKDOWN_V2)
    else:
        data_message = detailed_stats_coin(context.args[0])
        if data_message:
            update.message.reply_text(reply_to_message_id=update.message.message_id,
                                      text="`" + data_message + "`",
                                      parse_mode=ParseMode.MARKDOWN_V2)
        else:
            update.message.reply_text(TEXT.INVALID_COIN)

def trade(update, context):
    try:
        pic = create_trade_graph()
        context.bot.send_photo(reply_to_message_id=update.message.message_id,
                               chat_id=update.effective_chat.id,
                               photo=pic, caption="7 day trade history",
                               parse_mode=ParseMode.MARKDOWN_V2
                               )
    except Exception as e:
        print(e)
        print({"error": "Error in trade fetch"})

def main():
    bot_token = os.getenv('BOT_TOKEN')
    updater = Updater(token=bot_token, use_context=True, workers=8,
                      request_kwargs={'read_timeout': 10, 'connect_timeout': 10})
    dispatcher = updater.dispatcher

    # handlers
    price_handler = CommandHandler("price", price, run_async=True, filters=Filters.chat_type.supergroup)
    chart_handler = CommandHandler("chart", chart, run_async=True, filters=Filters.chat_type.supergroup)
    contract_handler = CommandHandler("contract", contract, run_async=True, filters=Filters.chat_type.supergroup)
    tweets_handler = CommandHandler("tweets", tweets, run_async=True, filters=Filters.chat_type.supergroup)
    simple_handler = CommandHandler("p", get_info_of_coin, run_async=True, filters=Filters.chat_type.supergroup)
    detailed_handler = CommandHandler("pc", get_detailed_info_of_coin, run_async=True, filters=Filters.chat_type.supergroup)
    trade_handler = CommandHandler("trade", trade, run_async=True, filters=Filters.chat_type.supergroup)
    dispatcher.add_handler(price_handler)
    dispatcher.add_handler(chart_handler)
    dispatcher.add_handler(contract_handler)
    dispatcher.add_handler(tweets_handler)
    dispatcher.add_handler(simple_handler)
    dispatcher.add_handler(detailed_handler)
    dispatcher.add_handler(trade_handler)

    jobQueue = updater.job_queue
    # jobQueue.run_repeating(repeat_tweet, interval=3600, first=10)
    jobQueue.run_repeating(repeat_price, interval=20, first=1)


    dispatcher.add_error_handler(error)


    updater.start_polling()
    # updater.start_webhook(listen="0.0.0.0", port=int(PORT), url_path=bot_token,
    #                      webhook_url=herokuAppUrl + bot_token)
    updater.idle()


if __name__ == '__main__':
    main()
