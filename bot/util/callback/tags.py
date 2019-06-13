from functools import reduce

from ..db import db
from ..keyboard import tags_keyboard

from .. import shared

def tags_callback(bot, message):
  available_tags = db.get_tags()

  tag = message.text
  id = message.chat.id

  if tag == 'Ready.':
    tags = shared.data[id]

    games = db.get_games(tags)

    text = 'Games I found based on your tags:\n\n'
    for game in games:
      price = ''
      if game['price'] == 0:
        price = 'Free to Play'
      else:
        price = '$' + str(game['price'] / 100)

      text += '[{}]({})\n{}\n*{}*\n\n'.format(
        game['name'],
        game['link'],
        reduce(lambda x, y: x + ', ' + y, game['tags']),
        price
      )

    bot.send_message(id, text, parse_mode="markdown")

    if id in shared.functions:
      del shared.functions[id]

    if id in shared.data:
      del shared.data[id]

    return

  if tag not in available_tags:
    bot.send_message(id, "I couldn't find anything with this tag, please try again.")
    return

  if id in shared.data:
    if tag in shared.data[id]:
      bot.send_message(id, 'You have already chosen this tag. Choose another one from the list below and press "Ready.".')
      return

    shared.data[id].append(tag)
  else:
    shared.data[id] = [tag]

  markup = tags_keyboard(shared.data[id])

  current_tags = reduce(lambda x, y: x + ', ' + y, shared.data[id])

  bot.send_message(id, 'Current list of tags: \n{}.\n\n You can add more tags or press the "Ready." button to start searching.'.format(current_tags), reply_markup=markup)
