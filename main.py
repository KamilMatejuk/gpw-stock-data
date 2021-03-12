import re
import ssl
import json
import certifi
import requests
import datetime
import urllib.request
from lxml import html, etree
from data_static import setup
from data_changing import getAllChangingData

from my_io import getData
from data_changing import graphAdvanced, graphSimple



if __name__ == '__main__':
    ### get not changing data from html file
    # setup('data_tickers.html')
    ### get changing data based on tickers
    # getAllChangingData()
    pass
