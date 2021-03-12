import re
import ssl
import json
import certifi
import requests
import datetime
import urllib.request
from lxml import html, etree


def saveData(data):
    with open('data.json', 'w+') as f:
        json.dump({
            'stocks': data
        }, f, indent = True,  ensure_ascii=False)


def getData():
    with open('data.json', 'rb') as f:
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

    # links to extrenal websites
    print('\033[33;1mGetting external links ...\033[0m')
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
    data = list(map(links, data))

    saveData(data)
    

def getChangingData():
    data = getData()
    
    # articles
    print('\033[33;1mGetting articles ...\033[0m')
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
                date = str(etree.tostring(date), 'ascii')
                date = date[13:19].replace(',', '')
                day, month = date.split(' ')
                months = ['sty', 'lut', 'mar', 'kwi', 'maj', 'cze', 'lip', 'sie', 'wrz', 'lis', 'gru']
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
            table = root.xpath('/html/body/div[1]/div[2]/div/div[1]/div[3]/div/div/div/div[3]/div/div/div/table/tbody')[0].findall('.//tr')
            date_str = datetime.datetime.strftime(datetime.datetime.today(), "%d.%m.%Y")
            for row in table:
                try:
                    row_str = str(etree.tostring(row), 'utf-8')
                    if 'divider' in row_str:
                        date_str = row.find('.//td').text_content().replace('/', '.')
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
    data = list(map(articles, data))
    saveData(data)
    return

    # predictions
    print('\033[33;1mGetting predictions ...\033[0m')
    def prediction(d):
        url = f'https://stooq.pl/q/g/?s={d["ticker"]}'
        resp = requests.get(url)
        with open('test.html', 'w+') as f:
            f.write(str(resp.text))
        root = html.fromstring(resp.text)
        tables = root.findall('.//table')
        table = str(etree.tostring(tables[38]), 'utf-8').split('(')
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
        root = html.fromstring(resp.text)
        tables = root.findall('.//table')
        row = tables[25].findall('.//tr')
        avg = str(etree.tostring(row[14]), 'utf-8').split('<td>')[1]
        avg = avg[:avg.find('</')].replace(',', '')
        if 'mld' in avg:
            avg = int(float(avg.split(' ')[0]) * 1000000000)
        elif 'mln' in avg:
            avg = int(float(avg.split(' ')[0]) * 1000000)
        d['average_daily_volume'] = abs(avg)
        print(d['ticker'])
        return d
    data = list(map(avgVolume, data))

    saveData(data)

### get not changing data from html file
# setup('data_tickers.html')
### get changing data based on tickers
getChangingData()


def getStockGraph(ticker, timeframe):
    # TODO dodać graf ze strony https://www.marketscreener.com/quote/stock/11-BIT-STUDIOS-S-A-25398936/ (graf zaawansowany)
    times = ['1d', '3d', '5d', '10d', '1m', '3m', '5m', '1r']
    if timeframe not in times:
        raise ValueError
    url = f'https://stooq.pl/c/?s={ticker.lower()}&c={timeframe}&t=l&a=lg'
    urllib.request.urlretrieve(url, f'graphs/{ticker}.png')
