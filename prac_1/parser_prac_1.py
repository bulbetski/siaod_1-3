import urllib.request
from bs4 import BeautifulSoup
import csv


MAIN_URL = "https://www.audit-it.ru/currency/daily_curs.php?monthStart=2&yearStart=2010&monthEnd=2&yearEnd=2020&currency=USD&currencyTable=USD%2CEUR%2CCZK"


def get_html(url):
    response = urllib.request.urlopen(url)
    return response.read()


def parse(html):
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('tbody')
    rows = table.find_all('tr')

    exchange_rate = []

    for row in rows:
        cols = row.find_all('td')
        exchange_rate.insert(0, {
            'date': cols[0].text,
            'USD': cols[1].text.strip()
        })
    return exchange_rate


def save(exchange_rate, path):
    with open(path, 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(('date', 'USD'))
        writer.writerows(
            (er['date'], er['USD']) for er in exchange_rate
        )


data = parse(get_html(MAIN_URL))
save(data, 'exchange_rate.csv')
