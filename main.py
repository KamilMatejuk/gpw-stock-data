import re
import ssl
import json
import lxml
import certifi
import requests
import urllib.request


def saveData(file, data):
    with open(file, 'w+') as f:
        json.dump({
            'stocks': data
        }, f, indent = True,  ensure_ascii=False)


def getData(file):
    with open(file, 'rb') as f:
        data = json.load(f)
    return data['stocks']


# @param file containing options tag from html
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
    def tickers(d):
        try:
            url = f'https://stooq.pl/q/g/?s={d["name"]}'
            resp = requests.get(url)
            root = lxml.html.fromstring(resp.text)
            font = str(lxml.etree.tostring(root.find('.//font[@id = "f16"]').getparent()), 'utf-8')
            ticker = re.split(r'\(|\)', font)
            d['ticker'] = ticker[1]
        except Exception as e:
            if type(e) == KeyboardInterrupt:
                exit(0)
            d['ticker'] = d['name']
        print(d['ticker'])
        return d
    data = list(map(tickers, data))

    # basic data
    print('\033[33;1mGetting financials ...\033[0m')
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
    data = list(map(financials, data))

    # saveData('tickets_data_static.json', data)
    

def getChangingData():
    stocks = getData('tickets_data.json')
    data = [{'ticker': s['ticker']} for s in stocks]
    
    # articles
    print('\033[33;1mGetting articles ...\033[0m')
    def articles(d):
        url = f'https://stooq.pl/q/g/?s={d["ticker"]}'
        resp = requests.get(url)
        root = lxml.html.fromstring(resp.text)
        table = root.xpath('//*[@id="f13"]/tr/td[1]/table[2]')[0].findall('.//tr')
        articles = []
        for row in table:
            link = row.find('.//a')
            date = row.find('.//font[@id = "a"]')
            if link is None or date is None:
                continue
            text = str(lxml.etree.tostring(link), 'ascii')[1:]
            url = 'https://stooq.pl/n' + text[9:text.find('>')-1].replace('&amp;', '&')
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
            date = str(lxml.etree.tostring(date), 'ascii')
            day = date[13:19].replace(',', '')
            articles.append({
                'title': title,
                'url': url,
                'day': day
            })
        d['articles'] = articles[:10]
        print(d['ticker'])
        return d
    data = list(map(articles, data))

    # predictions
    print('\033[33;1mGetting predictions ...\033[0m')
    def prediction(d):
        url = f'https://stooq.pl/q/g/?s={d["ticker"]}'
        resp = requests.get(url)
        with open('test.html', 'w+') as f:
            f.write(str(resp.text))
        root = lxml.html.fromstring(resp.text)
        tables = root.findall('.//table')
        table = str(lxml.etree.tostring(tables[38]), 'utf-8').split('(')
        up = table[1].split(')')[0]
        same = table[2].split(')')[0]
        down = table[3].split(')')[0]
        d['predictions'] = {
            'up': up,
            'same': same,
            'down': down
        }
        print(d['ticker'])
        return d
    data = list(map(prediction, data))

    # average volume (over 3 months)
    print('\033[33;1mGetting volume ...\033[0m')
    def avgVolume(d):
        url = f'https://stooq.pl/q/g/?s={d["ticker"]}'
        resp = requests.get(url)
        root = lxml.html.fromstring(resp.text)
        tables = root.findall('.//table')
        row = tables[25].findall('.//tr')
        avg = str(lxml.etree.tostring(row[14]), 'utf-8').split('<td>')[1]
        avg = avg[:avg.find('</')].replace(',', '')
        if 'mld' in avg:
            avg = int(float(avg.split(' ')[0]) * 1000000000)
        elif 'mln' in avg:
            avg = int(float(avg.split(' ')[0]) * 1000000)
        d['average_daily_volume'] = abs(avg)
        print(d['ticker'])
        return d
    data = list(map(avgVolume, data))

    saveData('tickets_data_changing.json', data)

### get not changing data from html file
# setup('data.html')
### get changing data based on tickers
# getChangingData()

