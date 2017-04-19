from bs4 import BeautifulSoup as bs
import requests
import re

url = 'http://sofifa.com/players?offset=0'


def soup_maker(url):
    r = requests.get(url)
    markup = r.content
    soup = bs(markup, "lxml")
    return soup


def find_top_players(soup):
    table = soup.find('table', {'class': 'table-striped'})
    tbody = table.find('tbody')
    all_a = tbody.find_all('a', {'class': ''})
    return(['http://sofifa.com' + player['href'] for player in all_a])

soup = soup_maker(url)
player_urls = find_top_players(soup)
