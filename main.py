from flask import Flask, request, send_file
app = Flask(__name__)

from data_static import setup
from data_changing import getAllChangingData
from webpages import mainPage, stockPage


@app.route('/')
def main():
    reload = request.args.get('reload')
    if reload:
        reload = reload.split(',')
        reload = [r for r in reload if r in ['articles', 'predictions', 'volume', 'graphs']]
    return mainPage(reload)


@app.route('/<ticker>')
def stock(ticker):
    return stockPage(ticker)


@app.route('/graphs/<img>')
def image(img):
    return send_file('graphs/' + img, mimetype='image/png')


if __name__ == '__main__':
    ### get not changing data from html file
    # setup('data.html')
    ### get changing data based on tickers
    # getAllChangingData()
    app.run()