import sys
from my_io import getData, saveData
from data_changing import getAllChangingData, getChangingData


def mainPage(reload):
    if reload:
        getAllChangingData(reload)
    data = getData()
    data = sortByPrediction(data)
    html = f'<div class="grid">'
    for d in data:
        html += getStockSummary(d)
    html += '</div>'
    return wrapHtml(html, title='GPW Stocks', style=getStyle())


def stockPage(ticker, reload):
    # find stock instance
    stock = None
    for d in getData():
        if d['ticker'] == ticker:
            stock = d
            break
    if stock is None:
        return f'Error: couldnt find ticker {ticker}'
    # reload data
    if reload:
        getChangingData(stock, reload)
    # create html
    try:
        daily_volume = 100 * int(stock["average_daily_volume"]) / stock['number_of_shares']
    except:
        daily_volume = 0
    buy = stock["predictions"]["buy"]
    sell = stock["predictions"]["sell"]
    css = 'green' if buy > sell else 'red'
    html = f'''<div class="main">
            <div>
                <img id="graph-img" src="graphs/{stock["ticker"]}-5d-simple.png">
                <div class="graph-btns">
                    <p onclick=graph("{stock["ticker"]}-1d-simple")>1d</p>
                    <p onclick=graph("{stock["ticker"]}-5d-simple")>5d</p>
                    <p onclick=graph("{stock["ticker"]}-1m-simple")>1m</p>
                    <p onclick=graph("{stock["ticker"]}-1m-advanced")>advanced</p>
                </div>
            </div>
            <div class="bottom">
                <div class="data">
                    <p id="t">{stock["name"]} ({stock["ticker"]})<span class="sector">{stock["market_sector"]}</span></p>
                    <p id="d1">PE: {stock["PE"]}</p>
                    <p id="d2">Daily volume: {daily_volume:.2f} %</p>
                    <p id="d3" class="{css}">Buy ({buy}) - ({sell}) Sell</p>
                </div>
                <div class="articles">{getArticles(stock)}</div>
            </div>
        </div>'''
    return wrapHtml(html, title=f'({ticker}) {stock["name"]}', style=getStyle(), script=getScript())


def sortByPrediction(data):
    def prediction(d):
        buy = d['predictions']['buy']
        sell = d['predictions']['sell']
        if sell != 0:
            return float(buy / sell)
        else:
            return float(buy)
    data.sort(key=prediction)
    data.reverse()
    return data


def getStyle():
    with open('html/style.css') as f:
        style = f.read()
    return str(style)


def getScript():
    with open('html/script.js') as f:
        style = f.read()
    return str(style)


def getStockSummary(d):
    try:
        daily_volume = 100 * int(d["average_daily_volume"]) / d['number_of_shares']
    except:
        daily_volume = 0
    buy = d["predictions"]["buy"]
    sell = d["predictions"]["sell"]
    css = 'green' if buy > sell else 'red'
    return f'''
        <div class="stock">
            <a href="/{d["ticker"]}?reload=graphs" target="_blank"><img src="graphs/{d["ticker"]}-5d-simple.png"></a>
            <div class="data">
                <p id="t">{d["name"]} ({d["ticker"]})<span class="sector">{d["market_sector"]}</span></p>
                <p id="d1">PE: {d["PE"]}</p>
                <p id="d2">Daily volume: {daily_volume:.2f} %</p>
                <p id="d3" class="{css}">Buy ({buy}) - ({sell}) Sell</p>
                <a id="d4" href="/{d["ticker"]}?reload=graphs" target="_blank">Articles ({len(d["articles"])}) >>></a>
            </div>
        </div>
        '''


def getArticles(d):
    art = [a for a in d["articles"] if len(a['title']) > 0]
    html = f'<p>Articles ({len(art)})</p>'
    for a in art:
        html += f'<a href="{a["url"]}" target="_blank">({a["date"]}) {a["title"]}</a>'
    return html


def wrapHtml(html, title='Webpage', style='', script=''):
    return f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
    </head>
    <body>
        <style>{style}</style>
        {html}
        <script>{script}</script>
    </body>
    </html>
    '''
