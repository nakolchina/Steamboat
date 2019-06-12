import requests
import json

# NOTE: Allowed poll rate - 4 requests per second.
db_url = 'http://steamspy.com/api.php?request=appdetails&appid={}'
steam_url = 'https://store.steampowered.com/app/{}'

# appid - number
def get_stats(appid):
  url = db_url.format(appid)

  raw = requests.get(url).text
  data = json.loads(raw)

  stats = {}

  stats['name'] = data['name']
  stats['link'] = steam_url.format(appid)
  stats['price'] = data['price'] # in dollars
  stats['positive_reviews'] = data['positive']

  rating = data['owners'].split('.')

  lowest = int(rating[0].strip().replace(',', ''))
  highest = int(rating[-1].strip().replace(',', ''))

  stats['average_owners'] = int((lowest + highest) / 2)

  # get only 3 tags from each game
  stats['tags'] = list(data['tags'].keys())[0:3]

  return stats
