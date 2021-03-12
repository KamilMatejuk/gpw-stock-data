import re
import ssl
import certifi
import requests
import urllib.request
from lxml import html, etree
from my_io import saveData


"""
Checks a stock ticker, based on company name,
using stooq.pl
"""
def tickers(d):
    try:
        url = f'https://stooq.pl/q/g/?s={d["name"]}'
        resp = requests.get(url)
        root = html.fromstring(resp.text)
        font = str(etree.tostring(root.find('.//font[@id = "f16"]').getparent()), 'utf-8')
        ticker = re.split(r'\(|\)', font)
        d['ticker'] = ticker[1]
    except Exception as e:
        if type(e) == KeyboardInterrupt:
            exit(0)
        d['ticker'] = d['name']
    print(d['ticker'])
    return d


"""
Adds a list of financial metrics of a given stock,
from gpw.pl
"""
def financials(d):
    try:
        context=ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        # context.set_ciphers('HIGH:!DH:!aNULL')
        context.set_ciphers('DEFAULT@SECLEVEL=1')
        url = f'https://www.gpw.pl/ajaxindex.php?start=indicatorsTab&format=html&action=GPWListaSp&gls_isin={d["code"]}&lang=EN'
        resp = str(urllib.request.urlopen(url=url, context=context).read(), 'utf-8')
        resp = resp.replace('\t', '').replace('\n', '').replace('  ', '').split('td')
        d['market_sector'] = resp[5].replace('>', '').replace(' </', '').replace('</', '').replace('&amp;', '&')
        d['number_of_shares'] = int(resp[7].replace('>', '').replace(' </', '').replace('</', '').replace(',', ''))
        d['market_value_mln'] = float(resp[9].replace('>', '').replace(' </', '').replace('</', '').replace(',', ''))
        d['PE'] = float(resp[13].replace('>', '').replace(' </', '').replace('</', '').replace(',', ''))
        print(d['ticker'])
    except Exception as e:
        if type(e) == KeyboardInterrupt:
            exit(0)
        d['PE'] = 0
        print('error for', d['name'])
    return d


"""
Adds a list of links to external websites containing info about the stock,
such as infostrefa.com and marketscreener.com
"""
def links(d):
    try:
        # infostrefa
        url = f'http://infostrefa.com/infostrefa/pl/wiadomosci/szukaj/1?keyword={d["name"]}'
        resp = requests.get(url)
        root = html.fromstring(resp.text)
        node = root.xpath('/html/body/div[1]/div[2]/div/div[1]/div[3]/div/div/div/div[6]/div[1]/div/div[3]/div/div/table/tbody/tr[2]/td[1]/a')[0]
        a = str(etree.tostring(node), 'utf-8')
        link1 = 'http://infostrefa.com' + a.split('"')[1]
        # marketscreener
        name = d["name"].lower().replace(' ', '')
        url = f'https://www.marketscreener.com/search/?lien=recherche&mots={name}&RewriteLast=recherche&noredirect=0&type_recherche=0'
        resp = requests.get(url)
        root = html.fromstring(resp.text)
        node = root.find('.//*[@id="ALNI0"]').findall('.//a')[0]
        a = str(etree.tostring(node), 'utf-8')
        link2 = 'https://www.marketscreener.com/' + a.split('"')[1]
        # all
        d['links'] = {
            'infostrefa': link1,
            'marketscreener': link2
        }
    except:
        d['links'] = {
            'infostrefa': link1,
            'marketscreener': ''
        }
    print(d['ticker'])
    return d


"""
Runs all the methods above, to convert a html with data downloaded
from oficial chellange website into a json containing most important,
unchanging data about each stock
"""
def setup(file):
    # codes and names
    print('\033[33;1mReading codes and names from file ...\033[0m')
    data = []
    with open(file, 'r') as f:
        for line in f.readlines():
            l = re.split('"|<|>', line)
            if 'BETA' not in line and 'ETF' not in line:
                data.append({
                    'code': l[2],
                    'name': l[6]
                })
    # tickers
    print('\033[33;1mGetting tickers ...\033[0m')
    data = list(map(tickers, data))
    # basic data
    print('\033[33;1mGetting financials ...\033[0m')
    data = list(map(financials, data))
    # links to extrenal websites
    print('\033[33;1mGetting external links ...\033[0m')
    data = list(map(links, data))
    saveData(data)