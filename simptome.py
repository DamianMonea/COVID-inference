import os
import json
import argparse
import sklearn
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from constants import *
import re


def main():
    config = {}
    with open("config.json", "r") as config_file:
        config = json.load(config_file)
    df = pd.read_excel(config[TRAIN_PATH], na_values=None)
    data = df.iloc[:].values

    list = []
    for entry in data:
        val = re.split("^\s+|\s*,\s*|\s+$", str(entry[4]))

        for i in val:
            i = i.lower()
            if i != '':
                if i[0] != ' ' and i[0] != 'n':
                    ok = 0
                    for j in list:
                        if j == i:
                            ok = 1
                    if ok == 0:
                        list.append(i)
    dict = {}
    i = 0
    nr = 0
    while i < len(list) - 1:
        new = []
        for j in list[i: len(list) - 1]:
            k = 0
            value = ''
            for c in j:
                if k < len(list[i]) and c == list[i][k]:
                    k += 1
                elif k > 4:
                    value = j
                    break
                else:
                     k = 0
            if value != '':
                new.append(j)
                list.remove(j)
        if len(new) > 1:
            new.append(list[i])
            dict[list[i]] = new
            nr += 1
            list.remove(list[i])
        i += 1
    print(parse_simptoms("ameteli greturi parestezii"))



    pass
def search(index, simptoms, simptom):

    j = 0
    miss = 0
    i = index
    if simptom[0] == '<':
        res = simptoms
    while i < len(simptoms):
        if simptoms[i] == simptom[j] and j < len(simptom) - 1:
            j += 1
        elif j > len(simptom) - 2 and len(simptom) > 4:
            while i < len(simptoms) and simptoms[i] != ' ' and simptoms[i] != ',':
                i += 1
            while i < len(simptoms) and (simptoms[i] == ' ' or simptoms[i] == ','):
                i += 1
            i -= 1
            return (i, True, j)
        elif j > 1 and miss == 0:
            miss = 1
            j += 1
            i -= 1
        else:
            j = 0
        i += 1

    return (0, False)

def search_value(simptoms, simptom):

    res = []
    if (" " in simptom):
        res = re.split("\s+", simptom)
    if len(res) == 0:
        x = search(0,simptoms, simptom)
        if x[1]:
            print(x, simptom)
        return x[1]
    else:
        index = 0
        list = []
        nr = 0
        score = 0
        length = 0
        for i in res:
            val = search(index, simptoms, i)
            list.append(val)
            length += len(i) - 1
            if val[1]:
                index = val[0]
                nr += 1
                score += val[2]

        if (score > length/(len(res) - 1)):
            print(list, simptom, score, length/(len(res) - 1))
            return True

    return False


def parse_simptoms(simptoms):
    with open('simptome.json') as f:
        data = f.read()


    # reconstructing the data as a dictionary
    dict = json.loads(data)
    print(dict)
    list = [0] * (len(dict) - 1)
    for key in dict:
        if search_value(simptoms, key):
            list[dict[key]] = 1

    return list



if __name__ == "__main__":
    main()