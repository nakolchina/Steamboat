from telebot import types

from .db import db

def tags_keyboard(current_tags = []):
  markup = types.ReplyKeyboardMarkup()

  done = types.KeyboardButton('Ready.')
  markup.row(done)

  available_tags = db.get_tags()

  for tag in available_tags:
    if tag not in current_tags:
      button = types.KeyboardButton(tag)

      markup.row(button)

  return markup
