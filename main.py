import telebot
import stocks_data
import wsb_sentiment
import datetime as dt
import json
from codecs import unicode_escape_decode as udc

#TELE_TOKEN = '1946902293:AAH6DM0HtddNlMcn5DiZ3FmtBkI0nNIECnY'
#TELE_TOKEN = '1971216795:AAG0uaCijzAIQZghgYVlXJJ90ZPpc8ksaek'


def main():
    
    with open("config.json", 'r') as config_file:
        config = json.load(config_file)
    TELE_TOKEN = config["telebot"]["token_api"]
    welcome_msg = udc(config["telebot"]["welcome_msg"])[0]
    help_msg = udc(config["telebot"]["help_msg"])[0]
    ticker_not_found_msg = udc(config["telebot"]["ticker_not_found_msg"])[0]
    after_sentiment_msg = udc(config["telebot"]["after_sentiment_msg"])[0]
    ask_if_donate_msg = udc(config["telebot"]["ask_if_donate_msg"])[0]
    no_donate_reply_msg = udc(config["telebot"]["no_donate_reply_msg"])[0]
    donate_grab_url = config["telebot"]["donate_grab_url"]
    donate_paylah_url = config["telebot"]["donate_paylah_url"]
    
    bot = telebot.TeleBot(TELE_TOKEN)
    print(bot.get_me())

    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        bot.send_message(message.chat.id, welcome_msg)

    @bot.message_handler(commands=['help'])
    def send_help(message):
        bot.send_message(message.chat.id, help_msg)

    @bot.message_handler(commands=['donate'])
    def ask_if_donate(message):
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, \
                                                   one_time_keyboard=True)
        support_option_1 = telebot.types.KeyboardButton("/yes_donate")
        support_option_2 = telebot.types.KeyboardButton("/no_donate")
        markup.row(support_option_1, support_option_2)
        bot.send_message(message.chat.id, ask_if_donate_msg, \
                         reply_markup=markup)

    @bot.message_handler(commands=['yes_donate'])
    def send_donate_options(message):
        markup = telebot.types.InlineKeyboardMarkup()
        payment_option_1 = telebot.types.InlineKeyboardButton('Grab', \
            url=donate_grab_url)
        payment_option_2 = telebot.types.InlineKeyboardButton('PayLah', \
            url=donate_paylah_url)
        markup.row(payment_option_1, payment_option_2)
        bot.send_message(message.chat.id, \
            "Select your prefered payment mode below", reply_markup=markup)

    @bot.message_handler(commands=['no_donate'])
    def send_no_donate_reply(message):
        bot.send_message(message.chat.id, no_donate_reply_msg)

    @bot.message_handler(commands=['r_wsb'])
    def analyse_r_wsb(message):
        bot.send_photo(message.chat.id, \
                       photo=open('r_wallstreetbets_top_picks.jpg', 'rb'))
        bot.send_photo(message.chat.id, \
                       photo=open('r_wallstreetbets_sentiment.jpg', 'rb'))
        bot.send_message(message.chat.id, after_sentiment_msg)
        with open('chat_ids.txt', 'a') as ids_file:
            ids_file.writelines(dt.datetime.now().strftime('%Y%m%d %H:%M') + \
                                ' ' + str(message.chat.id) + ' \n/n')

    @bot.message_handler(commands=['r_stocks'])
    def analyse_r_stocks(message):
        bot.send_photo(message.chat.id, \
                       photo=open('r_stocks_top_picks.jpg', 'rb'))
        bot.send_photo(message.chat.id, \
                       photo=open('r_stocks_sentiment.jpg', 'rb'))
        bot.send_message(message.chat.id, after_sentiment_msg)
        with open('chat_ids.txt', 'a') as ids_file:
            ids_file.writelines(dt.datetime.now().strftime('%Y%m%d %H:%M') + \
                                ' ' + str(message.chat.id) + ' \n')

    @bot.message_handler(commands=['r_stockmarket'])
    def analyse_r_stockmarket(message):
        bot.send_photo(message.chat.id, \
                       photo=open('r_stockmarket_top_picks.jpg', 'rb'))
        bot.send_photo(message.chat.id, \
                       photo=open('r_stockmarket_sentiment.jpg', 'rb'))
        bot.send_message(message.chat.id, after_sentiment_msg)
        with open('chat_ids.txt', 'a') as ids_file:
            ids_file.writelines(dt.datetime.now().strftime('%Y%m%d %H:%M') + \
                                ' ' + str(message.chat.id) + ' \n')

    @bot.message_handler(commands=['r_investing'])
    def analyse_r_investing(message):
        bot.send_photo(message.chat.id, \
                       photo=open('r_investing_top_picks.jpg', 'rb'))
        bot.send_photo(message.chat.id, \
                       photo=open('r_investing_sentiment.jpg', 'rb'))
        bot.send_message(message.chat.id, after_sentiment_msg)
        with open('chat_ids.txt', 'a') as ids_file:
            ids_file.writelines(dt.datetime.now().strftime('%Y%m%d %H:%M') + \
                                ' ' + str(message.chat.id) + ' \n')

    @bot.message_handler(func=lambda m: True)
    def reply_and_plot(message):
        reply = stocks_data.get_stock_data(message)
        if reply:
            bot.reply_to(message, reply)
            bot.send_photo(message.chat.id, photo=open('stock.jpg', 'rb'))
        else:
            bot.reply_to(message, ticker_not_found_msg)
    bot.infinity_polling()

if __name__ == '__main__':
    main()


# ###!/usr/bin/env python
# # -*- coding: utf-8 -*-
# # This program is dedicated to the public domain under the CC0 license.

# """
# Simple Bot to reply to Telegram messages.

# First, a few handler functions are defined. Then, those functions are passed to
# the Dispatcher and registered at their respective places.
# Then, the bot is started and runs until we press Ctrl-C on the command line.

# Usage:
# Basic Echobot example, repeats messages.
# Press Ctrl-C on the command line or send a signal to the process to stop the
# bot.
# """

# import logging
# from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
# from telegram.ext import  Updater, CommandHandler, MessageHandler, Filters
# import telegram
# import stocks_data

# # Enable logging
# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#                     level=logging.INFO)
# logger = logging.getLogger(__name__)


# # Define a few command handlers. These usually take the two arguments update and
# # context. Error handlers also receive the raised TelegramError object in error.
# def start(update, context):
#     """Send a message when the command /start is issued."""
#     update.message.reply_text('type pm25 for PM2.5 reading at 5pm; \
#     type psi for PSI value at 5pm')

# def info(update, context):
#     """Give users info"""
#     update.message.reply('type /pm25 for PM2.5 readings at 5pm; \
#     type /psi for psi value at 5pm')

# def help(update, context):
#     """Send a message when the command /help is issued."""
#     update.message.reply_text('Help!')


# def echo(update, context):
#     """Echo the user message."""
#     # update.message.reply_text(update.message.text)
#     reply = stocks_data.view_stock(update.message.text)
#     # if reply:
#     #     update.message.reply_text(reply)
#     # else:
#     #     update.message.reply_text('check your ticker')
#     bot.send_photo('Untitled.png')


# def error(update, context):
#     """Log Errors caused by Updates."""
#     logger.warning('Update "%s" caused error "%s"', update, context.error)


# def main():
#     """Start the bot."""
#     # Create the Updater and pass it your bot's token.
#     # Make sure to set use_context=True to use the new context based callbacks
#     # Post version 12 this will no longer be necessary
#     bot = Bot('1975576863:AAHpnTbAASGVQ1A8vnTnBXxi99mXS2gD3is')
#     updater = Updater('1975576863:AAHpnTbAASGVQ1A8vnTnBXxi99mXS2gD3is', \
#     use_context=True)

#     # Get the dispatcher to register handlers
#     dp = updater.dispatcher

#     # on different commands - answer in Telegram
#     dp.add_handler(CommandHandler("start", start))
#     dp.add_handler(CommandHandler("help", help))

#     # on noncommand i.e message - echo the message on Telegram
#     dp.add_handler(MessageHandler(Filters.text, echo))

#     # log all errors
#     dp.add_error_handler(error)

#     # Start the Bot
#     updater.start_polling()

#     # Run the bot until you press Ctrl-C or the process receives SIGINT,
#     # SIGTERM or SIGABRT. This should be used most of the time, since
#     # start_polling() is non-blocking and will stop the bot gracefully.
#     updater.idle()


# if __name__ == '__main__':
#     main()