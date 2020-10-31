import datetime
from dateutil.parser import parse
from pandas.io.parsers import ParserError
import os
import json
import argparse
import sklearn
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from constants import *

date_array = [
    '2020-06-29 08:15:27.243860',
    'Jun 28 2020 7:40AM',
    'Jun 28 2020 at 7:40AM',
    'September 18, 2020, 22:19:55',
    'Sun, 05/12/2020, 12:30PM',
    'Mon, 21 March, 2010',
    '2020-03-12T10:12:45Z',
    '2020-06-29 17:08:00.586525+00:00',
    '2020-06-29 17:08:00.586525+05:00',
    'Tuesday , 6th September, 2020 at 4:30pm',
    '2020-04-28 00:00:00',
    '20.04.2020',
    'Medicina Interna 2',
    'NU',
    '21 04 2020',
    '29,04,2020',
    '43936',
    '08,05,2020',
    'BI Cicio Pop',
    '29,04.2020',
    '29.04,2020',
    '29,04. 2020',
    '4/9/2020  12:00:00 AM',
    '31..03.2020',
    'BIA / ATI II',
    '',
    'NEURO/ATIII',
    '10.02.020',
    '10.02 2022',
    '19.05,2020'
]

class dateCaledaristice:  
    def __init__(self, date, number):  
        self.date = date  
        self.number = number 

def diff_dates(date2):
    date1 = datetime.datetime(2020,1,1).date()
    return (date2-date1).days

def hasNumbers(inputString):
    contor = 0
    for char in inputString:
        if char.isdigit():
            contor = contor + 1
    if contor >= 4:
        return True
    else:
        return False

def parseTime(date_array, dictionar):
    for index in range(len(date_array)):
        
        new_date = str(date_array[index]).replace(',','.')
        print('Parsing: ' + new_date)
        if hasNumbers(new_date):
            try:
                dt = parse(new_date)
                print(dt.date())
                print('INT = ' , diff_dates(dt.date()))
                print('\n')
                dictionar.append(dateCaledaristice(date_array[index],diff_dates(dt.date())))
            except :
                print("Nu e format valid de data")
                print('INT = ' , -1)
                print('\n')
                dictionar.append(dateCaledaristice(date_array[index], -1))
        else: 
            print('INT = ' , -1)
            print('\n')
            dictionar.append(dateCaledaristice(date_array[index], -1))

def main():
    
    config = {}
    with open("config.json", "r") as config_file:
        config = json.load(config_file)
        df = pd.read_excel(config[TRAIN_PATH], na_values=None)
        # Store values in 2D array
        data = df.iloc[:].values
        dates = []
        for entry in data:
            try:
                coloane_date = entry[3]
                new_coloane_date = str(coloane_date).replace("nan", "nu")
                dates.append(new_coloane_date)
                print("S = ", new_coloane_date)
            except AttributeError as e:
                print(e)

    dictionar = []
    parseTime(dates, dictionar)
    index = 2
    for dic in dictionar:
        print("INDEX = ",index)
        print("-")
        print("Key: ", dic.date)
        print(" - ")
        print("Value: ", dic.number)
        print("------\n")
        index = index + 1
    
if __name__ == "__main__":
    main()