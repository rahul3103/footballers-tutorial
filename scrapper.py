from bs4 import BeautifulSoup as bs
import requests
import re

url = 'http://sofifa.com/players?offset=0'


fifa_stats = ['Crossing', 'Finishing', 'Heading Accuracy',
              'Short Passing', 'Volleys', 'Dribbling', 'Curve',
              'Free Kick Accuracy', 'Long Passing', 'Ball Control',
              'Acceleration', 'Sprint Speed', 'Agility', 'Reactions',
              'Balance', 'Shot Power', 'Jumping', 'Stamina', 'Strength',
              'Long Shots', 'Aggression', 'Interceptions', 'Positioning',
              'Vision', 'Penalties', 'Composure', 'Marking', 'Standing Tackle',
              'Sliding Tackle', 'GK Diving', 'GK Handling', 'GK Kicking',
              'GK Positioning', 'GK Reflexes']


def soup_maker(url):
    r = requests.get(url)
    markup = r.content
    soup = bs(markup, 'lxml')
    return soup


def find_top_players(soup):
    final_details = {}
    table = soup.find('table', {'class': 'table-striped'})
    tbody = table.find('tbody')
    all_a = tbody.find_all('a', {'class': ''})
    for player in all_a:
        final_details['short_name'] = player.text
        final_details.update(player_all_details('http://sofifa.com' + player['href']))
        print(final_details)


def find_player_info(soup):
    player_data = {}
    player_data['image'] = soup.find('img')['data-src']
    player_data['full_name'] = soup.find('h1').text.split(' (')[0]
    span = soup.find('span', attrs={'class': None}).text.strip()
    dob = re.search('(\(.*)\)', span).group(0)
    player_data['dob'] = dob.replace('(', '').replace(')', '')
    infos = span.replace(dob + ' ', '').split(' ')
    player_data['pref_pos'] = infos[:infos.index('Age')]
    player_data['age'] = int(infos[infos.index('Age') + 1: -2][0])
    player_data['height'] = int((infos[infos.index('Age') + 2: -1][0]).replace('cm', ''))
    player_data['weight'] = int((infos[infos.index('Age') + 3:][0]).replace('kg', ''))
    return(player_data)


def find_player_stats(soup):
    player_data = {}
    info = re.findall('\d+', soup.text)
    player_data['rating'] = int(info[0])
    player_data['potential'] = int(info[1])
    player_data['value'] = int(info[2])
    player_data['wage'] = int(info[3])
    return(player_data)


def find_player_secondary_info(soup):
    player_data = {}
    player_data['preff_foot'] = soup.find('label', text='Preferred Foot')\
        .parent.contents[2].strip('\n ')
    player_data['club'] = soup.find_all('ul')[1].find('a').text
    player_data['club_pos'] = soup.find('label', text='Position')\
        .parent.find('span').text
    player_data['club_jersey'] = soup.find('label', text='Jersey number')\
        .parent.contents[2].strip('\n ')
    if soup.find('label', text='Joined'):
        player_data['club_joined'] = soup.find('label', text='Joined')\
            .parent.contents[2].strip('\n ')
    player_data['contract_valid'] = soup.find(
        'label', text='Contract valid until')\
        .parent.contents[2].strip('\n ')
    if len(soup.find_all('ul')) > 2:
        player_data['country'] = soup.find_all('ul')[2].find('a').text
    return(player_data)


def find_fifa_info(soup):
    player_data = {}
    divs_without_skill = soup[1].find_all('div', {'class': 'col-3'})[:3]
    more_lis = [div.find_all('li') for div in divs_without_skill]
    lis = soup[0].find_all('li') + more_lis[0]
    for li in lis:
        for stats in fifa_stats:
            if stats in li.text:
                player_data[stats.replace(' ', '_').lower()] = int(
                    (li.text.split(' ')[0]).replace('\n', ''))
    traits = soup[1].find('h4', text='Traits')
    if traits:
        player_data['traits'] = [li.text.replace('\xa0', '') for li in
            traits.parent.next_sibling.next_sibling.find_all('li')]
    specialities = soup[1].find('h4', text='Specialities')
    if specialities:
        player_data['specialities'] = [li.text.replace('\xa0', '') for li in
            specialities.parent.next_sibling.next_sibling.find_all('li')]
    return(player_data)


def player_all_details(url):
    all_details = {}
    soup = soup_maker(url)
    player_info = soup.find('div', {'class': 'player'})
    all_details.update(find_player_info(player_info))
    player_stats = soup.find('div', {'class': 'stats'})
    all_details.update(find_player_stats(player_stats))
    secondary_info = soup.find('div', {'class': 'teams'})
    all_details.update(find_player_secondary_info(secondary_info))
    fifa_info = soup.find_all('div', {'class': 'columns mb-20'})
    all_details.update(find_fifa_info(fifa_info))
    return(all_details)


soup = soup_maker(url)
find_top_players(soup)
