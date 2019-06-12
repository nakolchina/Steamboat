import sqlite3
import os

from functools import reduce

class Database:
  def __init__(self, path):
    self.path = path
    self.tags = []

    self.__create_tables__()

  def __create_tables__(self):
    with sqlite3.connect(self.path) as connection:
      cursor = connection.cursor()

      cursor.execute('''CREATE TABLE IF NOT EXISTS games (
        name              TEXT NOT NULL UNIQUE,
        link              TEXT NOT NULL UNIQUE,
        price             INT  NOT NULL,
        positive_reviews  INT  NOT NULL,
        average_owners    INT  NOT NULL,
        tags              TEXT NOT NULL
      )''')

      cursor.execute('''CREATE TABLE IF NOT EXISTS tags (
        name              TEXT NOT NULL UNIQUE
      )''')

      connection.commit()

  def add_tags(self, tags):
    args = list(map(lambda x: (x, ), tags))

    with sqlite3.connect(self.path) as connection:
      cursor = connection.cursor()
      cursor.executemany('INSERT INTO tags VALUES (?)', args)
      connection.commit()

  def get_tags(self):
    if len(self.tags) == 0:
      with sqlite3.connect(self.path) as connection:
        cursor = connection.cursor()

        cursor.execute('SELECT * FROM tags')
        self.tags = list(map(lambda x: x[0], cursor.fetchall()))

        connection.commit()

    return self.tags

  def add_game(self, game):
    tags = reduce(lambda x, y: x + ';' + y, game['tags'])

    args = (
      game['name'],
      game['link'],
      game['price'],
      game['positive_reviews'],
      game['average_owners'],
      tags,
    )

    with sqlite3.connect(self.path) as connection:
      cursor = connection.cursor()
      cursor.execute('INSERT INTO games VALUES (?, ?, ?, ?, ?, ?)', args)
      connection.commit()

  def get_games(self, tags):
    priority = {}

    for i in range(len(tags)):
      priority[tags[i]] = len(tags) - i

    games_raw = []

    with sqlite3.connect(self.path) as connection:
      cursor = connection.cursor()
      cursor.execute('SELECT * FROM games')
      games_raw = cursor.fetchall()
      connection.commit()

    games = []

    for element in games_raw:
      game = {}

      game['name'] = element[0]
      game['link'] = element[1]
      game['price'] = element[2]
      game['positive_reviews'] = element[3]
      game['average_owners'] = element[4]

      game['tags'] = element[5].split(';')
      game['points'] = 0

      for tag in game['tags']:
        if tag in priority:
          game['points'] += priority[tag]

      games.append(game)

    games = sorted(games, key=lambda x: (x['points'], x['positive_reviews'], x['average_owners']))

    return games[:-6:-1]

db = Database('db/games.db')
