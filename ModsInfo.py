import json
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os


# Print iterations progress
def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 *
                                                     (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end=printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()


data = ''


def checkname():
    name = 'warframeapimods'
    modscounter = 0
    with open(f"ModsJson/{name}.json", "r") as json_file:
        data = json.load(json_file)
        total = len(data)
        for mod in data:
            test = requests.get(
                f"https://warframe.fandom.com/wiki/" + mod["name"].replace(" ", "_"))
            modscounter = modscounter + 1
            percentagem = 100*(modscounter/total)
            print(f"\r {percentagem} %", end='\r')
            if test.status_code == 404:
                soup = BeautifulSoup(test.text, 'html.parser')
                h3 = soup.find(text="Did you mean")
                h1 = soup.find('h1', {"class": "page-header__title"})
                span = soup.find('span', {"class": "mw-headline"})
                soup2 = BeautifulSoup(str(span), 'html.parser')
                a = soup2.find('a')
                soupa = BeautifulSoup(str(a), 'html.parser')
                afinal = soupa.text
                mod['name'] = soupa.text
                json_file.close()

        os.remove(f"ModsJson/{name}.json")
        with open(f"ModsJson/{name}.json", "w") as json_file:
            json.dump(data, json_file, ensure_ascii=False)
            json_file.close()


def getMods():
    notableendo = []

    name = 'warframeapimods'
    modscounter = 0
    with open(f"ModsJson/{name}.json", "r") as json_file:
        data = json.load(json_file)
        total = len(data)
        printProgressBar(0, total, prefix='Progress:',
                         suffix='Complete', length=50)
        for mod in data:
            test = requests.get(
                f"https://warframe.fandom.com/wiki/" + mod["name"].replace(" ", "_"))
            if test.status_code != 200:
                continue
            img = BeautifulSoup(test.text, 'html.parser')
            finallink = img.find('a', {"class": "image image-thumbnail"})
            mod['imglink'] = finallink['href']
            soup = BeautifulSoup(test.text, 'html.parser')
            tableendo = soup.find("table", {"class": "emodtable"})
            if tableendo == None:
                notableendo.append(mod["name"])
                continue
            df_full = pd.read_html(str(tableendo))[0]

            mod['endo'] = df_full.to_dict('records')
            modscounter = modscounter + 1
            printProgressBar(modscounter, total, prefix='Progress:',
                             suffix='Complete', length=50)

    os.remove(f"ModsJson/{name}.json")
    with open(f"ModsJson/{name}.json", "w") as json_file:
        json.dump(data, json_file, ensure_ascii=False)
    print(notableendo)


# checkname()
getMods()
