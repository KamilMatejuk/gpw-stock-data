from my_io import getData, saveData
from data_changing import getAllChangingData


def mainPage(reload):
    if reload:
        getAllChangingData(reload)
    data = getData()
    html = f'<style>{getStyle()}</style><div class="grid">'
    for d in data:
        html += getStockSummary(d)
    html += '</div>'
    return html


def stockPage(ticker):
    return 't ' + ticker


def getStyle():
    with open('style.css') as f:
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
            <img src="graphs/{d["ticker"]}-5d-simple.png">
            <div class="data">
                <p id="t">{d["name"]} ({d["ticker"]})<span class="sector">{d["market_sector"]}</span></p>
                <p id="d1">PE: {d["PE"]}</p>
                <p id="d2">Daily volume: {daily_volume:.2f} %</p>
                <p id="d3" class="{css}">Buy ({buy}) - ({sell}) Sell</p>
                <a id="d4" href="/{d["ticker"]}" target="_blank">Articles ({len(d["articles"])}) >>></a>
            </div>
        </div>
        '''
    