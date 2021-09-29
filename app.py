from cred import Creds
from plugins import TEXT
from coingecko import print_full_info, detailed
from telegram.ext import Updater, CommandHandler, Filters
from telegram import ParseMode
import os
import time
from mongodb_count import increaseCount, get_counts
import asyncio
from pancake_latest_bitq import run_query
from web3api_price import getPrice
from make_graph import graph_create
import logging

PORT = int(os.environ.get('PORT', 5000))


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(update, context):
    first_name = update.message.chat.first_name
    print(update.message.chat)
    update.message.reply_text(TEXT.START.format(first_name))


def COIN(update, context):
    data_message = print_full_info("COIN")
    if data_message:
        print(update.effective_chat.id)
        update.message.reply_text(reply_to_message_id=update.message.message_id,
                                  text="`" + data_message + "`",
                                  parse_mode=ParseMode.MARKDOWN_V2)
    else:
        update.message.reply_text(TEXT.OOPS)
    try:
        increaseCount('COIN_cmd')
    except:
        pass


def full(update, context):
    if len(context.args) != 1:
        update.message.reply_text(reply_to_message_id=update.message.message_id,
                                  text="Please enter the command correctly\n\n" + "`" + "/p <CoinSymbol>" + "`",
                                  parse_mode=ParseMode.MARKDOWN_V2)
    else:
        data_message = print_full_info(context.args[0])
        if data_message:
            update.message.reply_text(reply_to_message_id=update.message.message_id,
                                      text="`" + data_message + "`",
                                      parse_mode=ParseMode.MARKDOWN_V2)
        else:
            update.message.reply_text(TEXT.INVALID_COIN)
    try:
        increaseCount('p_cmd')
    except:
        pass


def COINDetailed(update, context):
    data_message = detailed("COIN")
    # print(data_message)
    if data_message:
        print(update.effective_chat.id)
        # context.bot.send_photo(chat_id=update.message.chat_id, reply_to_message_id=update.message.message_id,
        #                        photo=img_url, caption="`" + data_message + "`",
        #                        parse_mode=ParseMode.MARKDOWN_V2)
        update.message.reply_text(reply_to_message_id=update.message.message_id,
                                  text="`" + data_message + "`",
                                  parse_mode=ParseMode.MARKDOWN_V2)
    else:
        update.message.reply_text(TEXT.OOPS)
    try:
        increaseCount('COIN_cmd')
    except:
        pass

CHATID = ''

def send_as_bot(update, context):
    # print(update.effective_chat.id)
    if update.message.reply_to_message is not None:
        context.bot.copy_message(chat_id=CHATID, from_chat_id=update.effective_message.chat_id
                                 , message_id=update.message.reply_to_message.message_id)
    text = update.message.text.replace("/sendCOINgrp", "")
    if text:
        context.bot.send_message(chat_id=CHATID, text=text)


def send_as_bot2(update, context):
    if update.message.reply_to_message is not None:
        context.bot.copy_message(chat_id=CHATID, from_chat_id=update.effective_message.chat_id
                                 , message_id=update.message.reply_to_message.message_id)
    text = update.message.text.replace("/sm", "")
    if text:
        context.bot.send_message(chat_id=CHATID, text=text)


def delete(update, context):
    if len(context.args) == 1:
        try:
            splitted_msg = context.args[0].split("/")
            messageId = splitted_msg[len(splitted_msg) - 1]
            context.bot.delete_message(chat_id=CHATID,
                                       message_id=messageId)
            update.message.reply_text(reply_to_message_id=update.message.message_id,
                                      text="Message deleted")
            # print(messageId)
        except:
            update.message.reply_text(reply_to_message_id=update.message.message_id,
                                      text="Message not deleted , argument wrong\ndel mesasage_link")
    else:
        update.message.reply_text(reply_to_message_id=update.message.message_id,
                                  text="Message not deleted \nNumber of arguments not equal to 1\ndel mesasage_link")


def stats(update, context):
    counts = get_counts()
    update.message.reply_text(reply_to_message_id=update.message.message_id,
                              text=f"`Statistics\n__________\n"
                                   f"🚀 /COIN   - {counts['COIN_cmd']}\n"
                                   f"🛰 /COIN - {counts['COIN_cmd']}\n"
                                   f"🚁 /p      - {counts['p_cmd']}`",
                              parse_mode=ParseMode.MARKDOWN_V2)


def latest_pair(update, context):
    if len(context.args) == 0:
        response = run_query(10)
        response = response['data']['ethereum']['arguments']
        text = ""
        if response:
            for data in response:
                addr = data['reference']['address']
                link = "https://bscscan.com/address/" + addr
                text += TEXT.PAIRADDRESS.format(addr, link) + "\n\n"
            update.message.reply_text(reply_to_message_id=update.message.message_id,
                                      text=text, parse_mode=ParseMode.MARKDOWN_V2)
        else:
            update.message.reply_text(reply_to_message_id=update.message.message_id,
                                      text="No response")
    elif len(context.args) == 1:
        try:
            response = run_query(int(context.args[0]))
            response = response['data']['ethereum']['arguments']
            text = ""
            if response:
                for data in response:
                    addr = data['reference']['address']
                    link = "https://bscscan.com/address/" + addr
                    text += TEXT.PAIRADDRESS.format(addr, link) + "\n\n"
                update.message.reply_text(reply_to_message_id=update.message.message_id,
                                          text=text, parse_mode=ParseMode.MARKDOWN_V2)
            else:
                update.message.reply_text(reply_to_message_id=update.message.message_id,
                                          text="No response")
        except Exception as e:
            update.message.reply_text(reply_to_message_id=update.message.message_id,
                                      text=e)
    else:
        update.message.reply_text(reply_to_message_id=update.message.message_id,
                                  text="argument length wrong\nEg: /latest 5")


def price(update, context):
    # print(update.effective_chat.id)
    timeout = 10
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
                                      text=f"⌛*Timeout enabled {timeout}s*\nTry after {int(timeout - timediff)} seconds",
                                      parse_mode=ParseMode.MARKDOWN_V2)
    else:
        runPrice = True

    if runPrice:
        wait_msg = update.message.reply_text(reply_to_message_id=update.message.message_id,
                                             text=TEXT.WAIT,
                                             parse_mode=ParseMode.MARKDOWN_V2)
        try:
            textP1, textP2 = getPrice()
            alltext = f'{textP1}{textP2}{TEXT.PRICETEXT}'.replace('=', '\=') \
                .replace('.', '\.').replace('|', '\|').replace('-', '\-')
            firstMsg = context.bot.edit_message_text(chat_id=update.effective_chat.id,
                                                     message_id=wait_msg.message_id,
                                                     text=alltext,
                                                     parse_mode=ParseMode.MARKDOWN_V2,
                                                     disable_web_page_preview=True)
            context.chat_data['startTime'] = time.time()
        except Exception as e:
            print(f'app.py Error 1 :{e}')
            context.bot.edit_message_text(chat_id=update.effective_chat.id,
                                          message_id=wait_msg.message_id,
                                          text="Sorry, failed to get data")
            context.chat_data['startTime'] = time.time()


def trades(update, context):
    try:
        pic= graph_create()
    except Exception as e:
        pic = ''
        print("Trades app.py error", e)
    if pic:
        text = f"📊 Trade Data 7 days"
        try:
            context.bot.send_photo(reply_to_message_id=update.message.message_id, chat_id=update.effective_chat.id,
                                   photo=pic, caption=text)
        except Exception as e:
            print("Trades app.py error2", e)
    else:
        text = f"Sorry failed to get data".replace('=', '\=') \
            .replace('.', '\.').replace('|', '\|').replace('-', '\-')
        try:
            update.message.reply_text(reply_to_message_id=update.message.message_id,
                                      text=text,
                                      parse_mode=ParseMode.MARKDOWN_V2)
        except Exception as e:
            print("Trades app.py error3", e)




def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)



def main():
    bot_token = Creds.bot_token
    updater = Updater(token=bot_token, use_context=True, workers=8)
    # allows to register handlers
    dispatcher = updater.dispatcher
    # handlers
    start_handler = CommandHandler("start", start, run_async=True)
    COIN_handler = CommandHandler("COIN", COIN, run_async=True, )
    detail_COIN_handler = CommandHandler("COIN", COINDetailed, run_async=True)
    full_info_handler = CommandHandler("p", full, run_async=True)

    price_handler = CommandHandler("price", price, run_async=True)
    trades_handler = CommandHandler("trades", trades, run_async=True)

    send_as_bot_handler = CommandHandler("sendCOINgrp", send_as_bot, run_async=True)
    send_as_bot_handler_my_grp = CommandHandler("sm", send_as_bot2, run_async=True)
    delete_message_handler = CommandHandler("del", delete, run_async=True)
    stats_handler = CommandHandler("stats", stats, run_async=True)
    latest_pair_handler = CommandHandler("latest", latest_pair, run_async=True,)

    # order of dispatched handler matters
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(COIN_handler)
    dispatcher.add_handler(full_info_handler)
    dispatcher.add_handler(detail_COIN_handler)
    dispatcher.add_handler(price_handler)
    dispatcher.add_handler(send_as_bot_handler)
    dispatcher.add_handler(send_as_bot_handler_my_grp)
    dispatcher.add_handler(delete_message_handler)
    dispatcher.add_handler(stats_handler)
    dispatcher.add_handler(latest_pair_handler)
    dispatcher.add_handler(trades_handler)


    dispatcher.add_error_handler(error)

    updater.start_polling()
    # updater.start_webhook(listen="0.0.0.0",
    #                       port=int(PORT),
    #                       url_path=bot_token, webhook_url='https://COIN-bot-telegram.herokuapp.com/' + bot_token)
    updater.idle()


if __name__ == '__main__':
    main()
