import tweepy
import time
import datetime
from bs4 import BeautifulSoup
import requests
import random
from dotenv import load_dotenv
import os

load_dotenv()
CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
ACCESS_KEY = os.getenv("ACCESS_KEY")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

fname = 'last_id.txt'

def store_last_id(last_id):
    with open(fname, 'w') as f:
        f.write(str(last_id))

def get_last_id():
    with open(fname, 'r') as f:
        return int(f.read().strip())

def reply_to_tweet():
    mentions = api.mentions_timeline(since_id = get_last_id(), tweet_mode = 'extended')

    soup = BeautifulSoup(requests.get('https://en.wikipedia.org/wiki/Wikipedia:On_this_day/Today').text,'lxml')
    events = []
    for tag in soup.find_all('div', class_='mw-body-content')[0].ul.find_all('li'):
        events.append(''.join(tag.find_all(text=True)))

    for mention in reversed(mentions):
        store_last_id(mention.id)
        print(str(mention.id) + ' ---   ' + mention.full_text)

        api.update_status(status ='@' + mention.user.screen_name + ' ' + datetime.datetime.now().strftime("%a %d %b %Y") + ' UTC+0530' + '\nOn this day:\n' + random.choice(events), in_reply_to_status_id = mention.id)

while True:
    reply_to_tweet()
    time.sleep(10)