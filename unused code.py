# def bitquery_price_fn(update, context):
#     wait_msg = update.message.reply_text(reply_to_message_id=update.message.message_id,
#                                          text=TEXT.WAIT,
#                                          parse_mode=ParseMode.MARKDOWN_V2)
#
#     result = asyncio.run(bitquery_price.run_query())
#     transaction_info = result['data']['ethereum']['dexTrades'][0]
#
#     buy_currency = transaction_info['buyCurrency']['symbol']
#     sell_currency = transaction_info['sellCurrency']['symbol']
#     buyAmount = transaction_info['buyAmount']
#     buyAmountInUsd = transaction_info['buyAmountInUsd']
#     sellAmount = transaction_info['sellAmount']
#     sellAmountInUsd = transaction_info['sellAmountInUsd']
#
#     if buy_currency == "COIN":
#         COIN_price_usd = sellAmountInUsd / buyAmount
#         COIN_price_otherCoin = sellAmount / buyAmount
#         otherCoin = sell_currency
#     else:
#         COIN_price_usd = buyAmountInUsd / sellAmount
#         COIN_price_otherCoin = buyAmount / sellAmount
#         otherCoin = buy_currency
#
#     context.bot.edit_message_text(chat_id=update.effective_chat.id,
#                                   message_id=wait_msg.message_id,
#                                   text='`' + TEXT.BITPRICE.format(COIN_price_usd,
#                                                                   otherCoin, COIN_price_otherCoin,
#                                                                   otherCoin) + '`',
#                                   parse_mode=ParseMode.MARKDOWN_V2)