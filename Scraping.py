from bs4 import BeautifulSoup
import requests

soup = BeautifulSoup(requests.get('https://en.wikipedia.org/wiki/Wikipedia:On_this_day/Today').text, 'lxml')
events = []
for tag in soup.find_all('div', class_= 'mw-body-content')[0].ul.find_all('li'):
    events.append(''.join(tag.find_all(text = True)))
