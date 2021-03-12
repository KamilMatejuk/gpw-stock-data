import json

"""
Saves data as a json file
"""
def saveData(data):
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