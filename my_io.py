import os
import json
from datetime import datetime


"""
Saves data as a json file
"""
def saveData(data):
    if os.path.exists('data.json'):
        date = datetime.now().strftime('%d.%m.%Y.%H:%M:%S')
        os.rename('data.json', f'data-old-{date}.json')
    with open('data.json', 'w+') as f:
        json.dump({
            'stocks': data
        }, f, indent = True,  ensure_ascii=False)


"""
Reads data from json file
"""
def getData():
    with open('data.json', 'rb') as f:
        data = json.load(f)
    return data['stocks']