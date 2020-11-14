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
        val = re.split("^\s+|\s*,\s*|\s+$", str(entry[6]))

        for i in val:
            print(parse_simptoms(i))
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



    pass
def search(index, simptoms, simptom):

    j = 0
    miss = 0
    i = index
    if i >= len(simptoms) - 1:
        return (0, False)

    if simptom[0] == '<':
        if simptoms[i] in '1234567890':
            nr = 0
            while i < len(simptoms) and simptoms[i] in '1234567890':
                nr = nr*10 + ord(simptoms[i]) - ord('0')
                i += 1
            return (i, True, nr);
        else:
            return (0, False)
    while i < len(simptoms):
        if simptoms[i] == simptom[j] and j < len(simptom) - 1:
            j += 1
        elif j > len(simptom) - 2 and len(simptom) > 4:
            while i < len(simptoms) and simptoms[i] != ' ' and simptoms[i] != ',':
                i += 1
            while i < len(simptoms) and (simptoms[i] == ' ' or simptoms[i] == ','):
                i += 1
            return (i, True, j)
        elif j == len(simptom) - 1 and miss == 0:
            while i < len(simptoms) and simptoms[i] != ' ' and simptoms[i] != ',':
                i += 1
            while i < len(simptoms) and (simptoms[i] == ' ' or simptoms[i] == ','):
                i += 1
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
    temp = 0
    if (" " in simptom):
        res = re.split("\s+", simptom)
    if len(res) == 0:
        x = search(0,simptoms, simptom)
        return (x[1], temp)
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
            if i[0] == '<':
                score += len(i)
                if val[1]:
                    temp = val[2]
                else:
                    temp = 38
            elif val[1]:
                index = val[0]
                nr += 1
                score += val[2]

        if (score > length/(len(res))):
            return (True, temp)

    return (False, temp)


def parse_simptoms(simptoms):
    with open('simptome.json') as f:
        data = f.read()


    # reconstructing the data as a dictionary
    dict = json.loads(data)
    list = [0] * (len(dict) - 1)
    list[22] = 36.5
    for key in dict:
        val = search_value(simptoms, key)
        if val[0]:
            if val[1] > 0:
                list[dict[key]] = val[1]
            else:
                list[dict[key]] = 1
    return list



if __name__ == "__main__":
    main()