import re

import pandas as pandas
import psycopg2
from bs4 import BeautifulSoup as bs
import requests

headers = {'accept': '*/*',
           'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0'}

base_url = 'https://www.playground.ru/games/?release=all&sort=follow_month&platform=pc&p=1'

def pg_parser(url, headers):

    con = psycopg2.connect(
        database='boythesda',
        user='postgres',
        password='729438165',
        host='localhost',
        port='',
    )
    print('Database opened successfully')
    cur = con.cursor()

    urls = []
    session = requests.Session()
    req = session.get(base_url, headers=headers)

    if req.status_code == 200:
        soup = bs(req.content, 'lxml')

        pagination = soup.find_all('ul', attrs={'class': 'pagination'})
        # p - номер последней страницы
        p = (pagination[0].find_all('a'))[-2].text
        # for i in range(1, int(p) + 1): ######################################################################################ЗАГЛУШКА
        for i in range(1, 3):
            url = f'https://www.playground.ru/games/?release=all&sort=follow_month&platform=pc&p={i}'
            if url not in urls:
                urls.append(url)

        for url in urls:
            req = session.get(url, headers=headers)
            soup = bs(req.content, 'lxml')
            divs = soup.find_all('div', attrs={'class': 'item'})
            for div in divs:
                game_url = (div.find('a')).get('href')
                game_info = get_game_info(game_url)

                load_data(cur, game_info)
        cur.close()
        con.commit()
        con.close()
    else:
        pass



def get_game_info(url):
    genres_in_game = []
    req = requests.get(url, headers)
    soup = bs(req.content, 'lxml')
    game_card = soup.find('div', attrs = {'class': 'gp-game-card-top'})

    title = game_card.find('h1', attrs={'class': 'gp-game-title', 'itemprop' : 'name'}).next_element.strip()

    genres = (game_card.find_all('a', attrs = {'class': 'item'}))
    for genre in genres:
        genres_in_game.append(genre.text.strip())

    try:
        releaseDate = pandas.to_datetime(game_card.find('time').text)
    except:
        releaseDate = None

    try:
        summary = game_card.find('div', attrs = {'id': 'fullDescription', 'class': 'full-description'}).text.rsplit()
    except:
        summary = game_card.find('div', attrs = {'class': 'description'}).text.rsplit()

    try:
        scoreCritics = float(game_card.find('span', attrs = {'itemprop': 'ratingValue'}).text)
    except: scoreCritics = float(0)

    try:
        scoreUsers = float(game_card.find('div', attrs = {'class': 'content readers'}).text)
    except: scoreUsers = float(0)

    try:
        publisher_name = game_card.find('span', attrs = {'itemprop' : 'publisher'}).text
    except: publisher_name = 'Издатель не указан'


    sysReqBlock = soup.find('div', attrs = {'class': 'gp-game-summary-requirements block'})
    try: HDD = sysReqBlock.find('span', text = 'Место на диске').next_sibling.replace(': ', '')
    except: HDD = 'Неизвестно'
    try: CPU = sysReqBlock.find('span', text = 'Процессор').next_sibling.replace(': ', '')
    except: CPU = 'Неизвестно'
    try: GPU = sysReqBlock.find('span', text = 'Видеокарта').next_sibling.replace(': ', '')
    except: GPU = 'Неизвестно'
    try:
        DDR = sysReqBlock.find('span', text = 'Оперативная память').next_sibling.replace(': ', '')
        DDR = int(DDR.split(' ')[0])
        if DDR > 16 : DDR = 1
    except: DDR = 0

    sys_req = {
        'HDD' : HDD,
        'CPU' : CPU,
        'GPU' : GPU,
        'DDR' : int(DDR),
    }
    info = {
        'title' : title,
        'summary' : summary,
        'releaseDate' : releaseDate,
        'genres' : genres_in_game,
        'scoreCritics' : scoreCritics,
        'scoreUsers' : scoreUsers,
        'sysReq' : sys_req,
        'publisher' : publisher_name
    }
    return info



def load_data(cur, game_info):

    cur.execute('INSERT INTO "PUBLISHER" (name, summary)'
                'VALUES (%s, %s);',
                (game_info['publisher'], 'Нет описания')
                )
    cur.execute('INSERT INTO "SYSREQ" (configuration_name, "HDD", "CPU", "GPU", "DDR")'
                'VALUES (%s, %s, %s, %s, %s);',
                (game_info['title'], game_info['sysReq']['HDD'], game_info['sysReq']['CPU'], game_info['sysReq']['GPU'], game_info['sysReq']['DDR'],)
                )

    cur.execute('INSERT INTO "GAME"(title, summary, "releaseDate", "scoreCritics", "scoreUsers", publisher_id, "sysReq_id")'
                'VALUES (%s, %s, %s, %s, %s,'
                '(SELECT "PUBLISHER".id from "PUBLISHER" where "PUBLISHER".name = %s),'
                '(SELECT "SYSREQ".id from "SYSREQ" where "SYSREQ".configuration_name = %s));',
                (game_info['title'], game_info['summary'], game_info['releaseDate'], game_info['scoreCritics'], game_info['scoreUsers'],
                game_info['publisher'], game_info['title'])
                )

    print('Ввод выполнен')

pg_parser(base_url, headers)