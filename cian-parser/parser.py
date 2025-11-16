import time
from random import *
from bs4 import BeautifulSoup
import requests
import json
import csv
from datetime import *
import re

from datetime import datetime, timedelta
import re

def edit_date(date_str):
    now = datetime.now()

    date_str = date_str.lower().strip()
    date_str = re.sub(r'^обновлено[:\s]*', '', date_str)
    date_str = date_str.strip()

    if date_str.startswith('сегодня'):
        return now.strftime('%d.%m.%y')

    elif date_str.startswith('вчера'):
        yesterday = now - timedelta(days=1)
        return yesterday.strftime('%d.%m.%y')

    else:
        months = {
            'янв': 1, 'фев': 2, 'мар': 3, 'апр': 4,
            'май': 5, 'июн': 6, 'июл': 7, 'авг': 8,
            'сен': 9, 'окт': 10, 'ноя': 11, 'дек': 12
        }

        match = re.search(r'(\d{1,2})\s+([а-я]+)(?:\s+(\d{4}))?', date_str)

        if match:
            day = int(match.group(1))
            month_str = match.group(2)
            year_str = match.group(3)

            month = months.get(month_str)
            if not month:
                return date_str

            if year_str:
                year = int(year_str)
            else:
                year = now.year

            try:
                date_obj = datetime(year, month, day)
                return date_obj.strftime('%d.%m.%y')
            except ValueError:
                return date_str

    return date_str

def cln(text):
    return text.replace('\xa0', ' ').strip()

headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 YaBrowser/25.8.0.0 Safari/537.36"
}

# card_urls=set()
# for i in range(1,55):
#     link=f"https://www.cian.ru/cat.php?currency=2&deal_type=sale&engine_version=2&house_material%5B0%5D=1&house_material%5B1%5D=2&house_material%5B2%5D=11&house_material%5B3%5D=12&house_material%5B4%5D=13&maxarea=350&maxprice=100000000&min_house_year=2024&minarea=120&minprice=15000000&object_type%5B0%5D=1&offer_type=suburban&p={i}&region=-1&sort=price_object_order"
#     page=requests.get(link,headers=headers)
#     soup=BeautifulSoup(page.content,"lxml")
#
#     with open('cianpars.html', 'w', encoding='utf-8') as f:
#         f.write(soup.prettify())
#
#     component_cards=soup.find_all('article', class_='_93444fe79c--container--Povoi _93444fe79c--cont--OzgVc')
#
#     print(link)
#     i=1
#     for card in component_cards:
#         print(i)
#         url=card.find('div',class_='_93444fe79c--card--ibP42').find('a').get('href')
#         i+=1
#         card_urls.add(url)
#
# for i in range(1,55):
#     link=f"https://www.cian.ru/cat.php?currency=2&deal_type=sale&engine_version=2&house_material%5B0%5D=1&house_material%5B1%5D=2&house_material%5B2%5D=11&house_material%5B3%5D=12&house_material%5B4%5D=13&maxarea=350&maxprice=100000000&min_house_year=2024&minarea=120&minprice=15000000&object_type%5B0%5D=1&offer_type=suburban&p={i}&region=-1&sort=total_price_desc"
#     page=requests.get(link,headers=headers)
#     soup=BeautifulSoup(page.content,"lxml")
#
#     with open('cianpars.html', 'w', encoding='utf-8') as f:
#         f.write(soup.prettify())
#
#     component_cards = soup.find_all('article', class_='_93444fe79c--container--Povoi _93444fe79c--cont--OzgVc')
#
#     print(link)
#     i = 1
#     for card in component_cards:
#         print(i)
#         url = card.find('div', class_='_93444fe79c--card--ibP42').find('a').get('href')
#         i += 1
#         card_urls.add(url)
# print(len(card_urls))
# with open('urlslist.txt', 'w', encoding='utf-8') as f:
#     for url in card_urls:
#         f.write(url+'\n')

# for i in range(1,35):
#     link=f"https://www.cian.ru/cat.php?deal_type=sale&engine_version=2&minprice=21000000&object_type%5B0%5D=1&offer_type=suburban&p={i}&region=1&sort=total_price_desc"
#     page=requests.get(link,headers=headers)
#     soup=BeautifulSoup(page.content,"lxml")
#
#     with open('cianpars.html', 'w', encoding='utf-8') as f:
#         f.write(soup.prettify())
#
#     component_cards=soup.find_all('div', class_='_93444fe79c--card--ibP42')
#
#     print(link)
#     i=1
#     for card in component_cards:
#         print(i)
#         url=card.find('a').get('href')
#         i+=1
#         card_urls.add(url)
# with open('urls.json', 'w', encoding='utf-8') as f:
#     json.dump(card_urls, f, ensure_ascii=False, indent=4)
with open('cianpars.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(
        (
            'URL',
            'Цена',
            'Дата публикации (обновления)',
            'Количество просмотров',
            'Площадь дома',
            'Этажность дома',
            'Площадь земельного участка',
            'Направление (шоссе)',
            'Удаленность от МКАД',
        )
    )
card_urls=[]
with open('urlslist.txt', 'r', encoding='utf-8') as f:
    for line in f:
        card_urls.append(line.strip())
print(f"Всего итераций: {len(card_urls)}")
i=1
for url in card_urls:
    print(f"Итерация №{i}, осталось {len(card_urls)-i}")
    i+=1
    home_page=requests.get(url, headers=headers)
    soup = BeautifulSoup(home_page.text, 'lxml')

    with open('cianpars.html', 'w', encoding='utf-8') as f:
        f.write(soup.prettify())

    price=soup.find('div', class_='xa15a2ab7--fc68b9--amount').find('span').text
    updated=soup.find('div', class_='xa15a2ab7--_821f5--container').find('span').text
    try:
        views=soup.find('div', class_='xa15a2ab7--_821f5--container').find('button').text
    except Exception:
        views='-'
    high=soup.find('ul', class_='xa15a2ab7--_9c9c7--highways').find_all('li')

    try:
        highways=''
        for highway in high:
            highways+=(highway.find('a').text)+', '
    except Exception:
        highways='-'

    try:
        distance=soup.find('ul', class_='xa15a2ab7--_9c9c7--highways').find('span').text
    except Exception:
        distance='-'

    url = cln(url)
    price = cln(price)
    updated = edit_date(cln(updated))
    views = cln(views).split(' ')[0]
    highways = cln(highways).strip()
    distance = cln(distance)
    area='-'
    floors='-'
    region='-'

    params=soup.find('div', class_='xa15a2ab7--_63197--container').find_all('div', class_='xa15a2ab7--_0523e--item')
    for param in params:
        key=param.find('p').text.strip()
        value=param.find('p', class_='xa15a2ab7--_7735e--color_text-primary-default xa15a2ab7--_2697e--lineHeight_6u xa15a2ab7--_2697e--fontWeight_normal xa15a2ab7--_2697e--fontSize_16px xa15a2ab7--_17731--display_block xa15a2ab7--dc75cc--text xa15a2ab7--dc75cc--text_letterSpacing__0').text.strip()
        if key=='Площадь':
            if param.parent.previous_sibling.find('h2').text.strip()=='О доме':
                area=cln(value)
            else:
                region=cln(value)
        elif key=='Количество этажей':
            floors=cln(value)

    with open('cianpars.csv', 'a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(
            (
            url, price, updated, views, area, floors, region, highways, distance
            )
        )
    #time.sleep(randrange(2,4))
print('Чикипуки')