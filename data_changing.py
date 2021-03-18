import re
import ssl
import time
import random
import certifi
import requests
import datetime
import urllib.request
from lxml import html, etree
from my_io import getData, saveData


"""
Adds a list of articles from latest 7 days to given stock,
from stooq.pl and infostrefa.com
"""
def articles(d):
    # stooq
    url = f'https://stooq.pl/q/g/?s={d["ticker"]}'
    resp = requests.get(url)
    root = html.fromstring(resp.text)
    table = root.xpath('//*[@id="f13"]/tr/td[1]/table[2]')[0].findall('.//tr')
    articles = []
    for row in table:
        try:
            link = row.find('.//a')
            date = row.find('.//font[@id = "a"]')
            if link is None or date is None:
                continue
            text = str(etree.tostring(link), 'ascii')[1:]
            url = 'https://stooq.pl/n' + \
                text[9:text.find('>')-1].replace('&amp;', '&')
            title = text[text.find('>')+2:text.find('<')]
            title = title.replace(r'&#197;&#131;', 'ń')
            title = title.replace(r'&#196;&#133;', 'ą')
            title = title.replace(r'&#195;&#179;', 'ó')
            title = title.replace(r'&#197;&#130;', 'ł')
            title = title.replace(r'&#197;&#188;', 'ż')
            title = title.replace(r'&#196;&#135;', 'ć')
            title = title.replace(r'&#196;&#153;', 'ę')
            title = title.replace(r'&#197;&#155;', 'ś')
            title = title.lower()
            date = str(etree.tostring(date), 'ascii')
            date = date[13:19].replace(',', '')
            day, month = date.split(' ')
            months = ['sty', 'lut', 'mar', 'kwi', 'maj',
                'cze', 'lip', 'sie', 'wrz', 'lis', 'gru']
            if month not in months:
                continue
            month = months.index(month) + 1
            month = f'0{month}' if month < 10 else str(month)
            date_str = f'{day}.{month}.{datetime.datetime.today().year}'
            date = datetime.datetime.strptime(date_str, '%d.%m.%Y')
            diff = (datetime.datetime.today() - date).days
            if diff <= 7:
                articles.append({
                    'title': title,
                    'url': url,
                    'date': date_str
                })
        except:
            continue
        # infostrefa
        url = d['links']['infostrefa']
        company_nr = re.split('/|,', url)[-2]
        url = 'http://infostrefa.com/infostrefa/pl/wiadomosci/wszystko/1?company=' + company_nr
        resp = requests.get(url)
        root = html.fromstring(resp.text)
        table = root.xpath(
            '/html/body/div[1]/div[2]/div/div[1]/div[3]/div/div/div/div[3]/div/div/div/table/tbody')[0].findall('.//tr')
        date_str = datetime.datetime.strftime(
            datetime.datetime.today(), "%d.%m.%Y")
        for row in table:
            try:
                row_str = str(etree.tostring(row), 'utf-8')
                if 'divider' in row_str:
                    date_str = row.find(
                        './/td').text_content().replace('/', '.')
                    date = datetime.datetime.strptime(date_str, '%d.%m.%Y')
                    diff = (datetime.datetime.today() - date).days
                    if diff > 7:
                        break
                else:
                    text = row.findall('.//td')[2].find('.//a')
                    text = str(etree.tostring(text), 'utf-8')
                    title = re.split('<|>', text)[2]
                    title = title.replace(r'&#197;&#131;', 'ń')
                    title = title.replace(r'&#196;&#133;', 'ą')
                    title = title.replace(r'&#195;&#179;', 'ó')
                    title = title.replace(r'&#197;&#130;', 'ł')
                    title = title.replace(r'&#197;&#188;', 'ż')
                    title = title.replace(r'&#196;&#135;', 'ć')
                    title = title.replace(r'&#196;&#153;', 'ę')
                    title = title.replace(r'&#197;&#155;', 'ś')
                    title = title.lower()
                    url = 'http://infostrefa.com' + text.split('"')[1]
                    if url not in [i['url'] for i in articles if i['url']]:
                        articles.append({
                            'title': title,
                            'url': url,
                            'date': date_str
                        })
            except:
                continue
    d['articles'] = articles[:10]
    print(d['ticker'], len(articles[:10]))
    return d


"""
Adds price prediction on given stock,
from stooq.pl and investing.com
"""
def prediction(d):
    # stooq.pl
    url = f'https://stooq.pl/q/g/?s={d["ticker"]}'
    resp = requests.get(url)
    root = html.fromstring(resp.text)
    tables = root.findall('.//table')
    table = str(etree.tostring(tables[38]), 'utf-8').split('(')
    up = int(table[1].split(')')[0])
    same = int(table[2].split(')')[0])
    down = int(table[3].split(')')[0])

    # investing.com
    try:
        url = f'https://pl.investing.com/equities/{d["name"].lower()}-technical'
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
        }
        resp = requests.get(url, headers=headers)
        with open('test.html', 'w+') as f:
            f.write(str(resp.text))
        root = html.fromstring(resp.text)
        buy1 = int(re.split('\(|\)', str(etree.tostring(
            root.xpath('//*[@id="maBuy"]')[0]), 'utf-8'))[1])
        buy2 = int(re.split('\(|\)', str(etree.tostring(
            root.xpath('//*[@id="tiBuy"]')[0]), 'utf-8'))[1])
        sell1 = int(re.split('\(|\)', str(etree.tostring(
            root.xpath('//*[@id="maSell"]')[0]), 'utf-8'))[1])
        sell2 = int(re.split('\(|\)', str(etree.tostring(
            root.xpath('//*[@id="tiSell"]')[0]), 'utf-8'))[1])
        d['predictions'] = {
            'buy': up + buy1 + buy2,
            'sell': same + down + sell1 + sell2
        }
        time.sleep(3)
    except:
        d['predictions'] = {
            'buy': up,
            'sell': same + down
        }
    print(d['ticker'])
    return d


"""
Adds average daily volume (from past 3 months) of given stock,
from stooq.pl
"""
def avgVolume(d):
    url = f'https://stooq.pl/q/g/?s={d["ticker"]}'
    resp = requests.get(url)
    root = html.fromstring(resp.text)
    tables = root.findall('.//table')
    row = tables[25].findall('.//tr')
    avg = str(etree.tostring(row[14]), 'utf-8').split('<td>')[1]
    avg = avg[:avg.find('</')].replace(',', '')
    if 'mld' in avg:
        avg = abs(int(float(avg.split(' ')[0]) * 1000000000))
    elif 'mln' in avg:
        avg = abs(int(float(avg.split(' ')[0]) * 1000000))
    d['average_daily_volume'] = avg
    print(d['ticker'])
    return d


"""
Downloads a simple price graph of given stock and timestamp,
from stooq.pl
"""
def graphSimple(d, timeframe):
    times = ['1d', '3d', '5d', '10d', '1m', '3m', '5m', '1r']
    if timeframe not in times:
        raise ValueError
    url = f'https://stooq.pl/c/?s={d["ticker"].lower()}&c={timeframe}&t=l&a=lg'
    urllib.request.urlretrieve(url, f'graphs/{d["ticker"]}-{timeframe}-simple.png')


"""
Downloads an advanced price graph of given stock and for specified number 
of months, from marketscreener.com
"""
def graphAdvanced(d, timeframe):
    link = d['links']['marketscreener']
    if len(link) > 0:
        nr = link.replace('/', '').split('-')[-1]
        url = f'https://www.zonebourse.com/zbcache/charts/ObjectChart.aspx?Name={nr}&Type=Custom&Intraday=1&Width=560&Height=360&Cycle=DAY1&Duration={timeframe}&Render=Candle&ShowCopyright=0&ShowName=0&Company=4Traders_us'
        urllib.request.urlretrieve(url, f'graphs/{d["ticker"]}-{timeframe}m-advanced.png')


"""
Downloads simple graphs for each stock
"""
def getAllSimpleGraphs(timeframe):
    for d in getData():
        graphSimple(d, timeframe)


"""
Runs most of above methods, to collect all current data,
and later use for filtering / displaing purposes 
"""
def getAllChangingData(reload):
    data = getData()
    if 'articles' in reload:
        print('\033[33;1mGetting articles ...\033[0m')
        data = list(map(articles, data))
    if 'predictions' in reload:
        print('\033[33;1mGetting predictions ...\033[0m')
        data = list(map(prediction, data))
    if 'volume' in reload:
        print('\033[33;1mGetting volume ...\033[0m')
        data = list(map(avgVolume, data))
    if 'graphs' in reload:
        print('\033[33;1mGetting graphs for 5d ...\033[0m')
        getAllSimpleGraphs('5d')
    saveData(data)