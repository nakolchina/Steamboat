import sys
import telebot

from util.fetch_games import fetch_games
from util.db import db

from util.callback.tags import tags_callback
from util.keyboard import tags_keyboard

import util.shared as shared

if len(sys.argv) > 1 and sys.argv[1] == 'fetch':
  fetch_games()
else:
  from telebot import apihelper
  apihelper.proxy = {'tg': 'tg://proxy?server=proxy.digitalresistance.dog&port=443&secret=d41d8cd98f00b204e9800998ecf8427e'}

  db.get_tags()

  print('starting...')

  token = '783040952:AAFUDFhHTvob4yV3uitVXmS1Hgat_xZJ8nQ'
  bot = telebot.TeleBot(token)

  @bot.message_handler(commands=['start'])
  def start(message):
    id = message.chat.id

    markup = tags_keyboard()
    bot.send_message(id, 'Hello! I’ll help you find new games based on your preferences. To start, choose the tags you’re interested in - the ones you choose first are the most important.', reply_markup=markup)

    if id in shared.data:
      del shared.data[id]

    shared.functions[id] = tags_callback

  @bot.message_handler(commands=['search'])
  def search(message):
    id = message.chat.id

    markup = tags_keyboard()
    bot.send_message(id, 'To start, choose the tags you’re interested in - the ones you choose first are prioritized.', markup)

    if id in shared.data:
      del shared.data[id]

    shared.functions[id] = tags_callback

  @bot.message_handler(commands=['help'])
  def help_handler(message):
    id = message.chat.id

    bot.send_message(id, '/start -- start over\n/search -- start searching games by tags\n/help -- list of available commands')

    if id in shared.functions:
      del shared.functions[id]

    if id in shared.data:
      del shared.data[id]

  @bot.message_handler(content_types=['text'])
  def text(message):
    id = message.chat.id

    if id in shared.functions:
      shared.functions[id](bot, message)
    else:
      bot.send_message(id, "Sorry, I don't understand. :(\n\nTo see what commands are available, type /help.")

  bot.polling()
