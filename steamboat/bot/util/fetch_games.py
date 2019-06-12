import requests
import json

import time

from .get_stats import get_stats
from .db import db

games_url = 'http://steamspy.com/api.php?request=top100owned'

def fetch_games():
  raw = requests.get(games_url).text
  data = json.loads(raw)

  appids = []

  if data == {}:
    # if the api goes down again, here's the first 100 games sorted by owners...
    appids = [570, 730, 440, 578080, 304930, 230410, 10, 275390, 444090, 272060, 240, 227940, 238960, 219990, 550, 340, 236390, 218620, 291550, 4000, 301520, 220, 400, 620, 360, 291480, 304050, 105600, 72850, 386360, 433850, 49520, 271590, 96000, 8930, 417910, 70, 359550, 80, 218230, 439700, 370910, 252950, 333930, 550650, 224260, 582660, 273110, 320, 381210, 420, 252490, 50, 130, 322330, 227300, 363970, 500, 30, 255710, 15700, 221380, 755790, 285800, 203160, 278360, 431960, 346110, 208090, 300, 10180, 219640, 380, 292030, 407530, 273350, 109600, 588430, 319630, 219740, 582010, 253710, 346900, 555570, 630, 252130, 377160, 20920, 339610, 204360, 238320, 1250, 7670, 231430, 40, 12210, 280790, 8870, 42910, 552500]
  else:
    appids = map(lambda x: data[x]['appid'], data.keys())

  games = []
  tags = set([])

  total = 100
  current = 1

  for appid in appids:
    print('\r{}/{}'.format(current, total), end='')

    # I don't know why, but the get_stats function works anyway
    game = get_stats(appid)
    games.append(game)

    tags.update(game['tags'])

    db.add_game(game)

    current += 1
    time.sleep(.25)

  db.add_tags(tags)

  print('\ndone.')
