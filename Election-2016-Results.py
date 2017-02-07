import json
import requests
import time
import threading
import pandas as pd

# Scraping the AP's live feed to get county level 2016 results

with open('./president_metadata.json') as pres_meta:
    pres_meta = json.load(pres_meta)
with open('./president.json') as pres:
    pres = json.load(pres)


def getResults():
    t = requests.get(
        "http://interactives.ap.org/interactives/2016/general-election/live-data/production/2016-11-08/president.json?={}".format(
            time.time()))
    pres = t.json()
    return pres


"http://interactives.ap.org/interactives/2016/general-election/live-data/production/2016-11-08/president.json?={}".format(
    str(time.time()).replace('.', ''))
pres['results']


def make_cand_dict():
    cand_dict = {}
    with open('./president_metadata.json') as pres_meta:
        pres_meta = json.load(pres_meta)
    for id, meta in pres_meta['cands'].items():
        cand_dict[id] = meta['fn']
    return cand_dict


def parse_results(pres, cand_dict):
    parsed_results = {}
    for state in pres['results'][1:]:
        p_res = list(zip(state['cand'], state['vote']))
        parsed_results[state['st'] + state['id']] = {'county': state['id'], 'state': state['st'], 'PR': state['pr'],
                                                     'vp': state['vp'],
                                                     'results': list(map(lambda x: (cand_dict[x[0]], x[1]), p_res))}
    return parsed_results




def parsePres():
    pres = getResults()
    cand_dict = make_cand_dict()
    parsed_results = parse_results(pres, cand_dict)
    return parsed_results


parsed_results = parsePres()

results = []
for state, race in parsed_results.items():
    for candidate in race['results']:
        if candidate[0] in ['Hillary Clinton', 'Donald Trump']:
            results.append([state, race['PR'], candidate[0], candidate[1]])

pd.DataFrame(results).to_csv('./results_16.csv')
