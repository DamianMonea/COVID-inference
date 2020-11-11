import tornado.web
import tornado.ioloop
import tornado.httpserver
import tornado.options
import os.path
import random
import string
import os, uuid
import json, csv
import datetime
import re
import datefinder
import os
import json
import argparse
import sklearn
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from constants import *
from dateutil.parser import parse
from pandas.io.parsers import ParserError
from dateparser.search import search_dates


__UPLOADS__ = "uploads/"

class Upload(tornado.web.RequestHandler):
    def post(self):
        fileinfo = self.request.files['filearg'][0]
        fname = fileinfo['filename']
        fh = open(__UPLOADS__ + fname, 'wb')
        fh.write(fileinfo['body'])
        main(__UPLOADS__ + fname)
        self.finish(fname + " is uploaded!! Check %s folder" %__UPLOADS__)
        fh.close();

class Userform(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class basicRequestHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world!!!!!!!!")

class staticRequestHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class querryStringRequestHandler(tornado.web.RequestHandler):
    def get(self):
        n = int(self.get_argument("n"))
        r = "odd" if n % 2 else "even"
        self.write("the number " + str(n) + " is " + r)

class resourceRequestHandler(tornado.web.RequestHandler):
    def get(self, id):
        self.write("Querrying tweet with id = " + id)


def main(filename):
    all_data_from_excel = {}
    json_data_list = []
    df = pd.read_excel(filename, na_values=None)
    data = df.iloc[:].values
    for entry in data:
        try:
            all_data_from_excel['instituția sursă'] = entry[0]
            all_data_from_excel['sex'] = entry[1]
            all_data_from_excel['vârstă'] = entry[2]
            all_data_from_excel['dată debut simptome declarate'] = entry[3]
            all_data_from_excel['simptome declarate'] = entry[4]
            all_data_from_excel['dată internare'] = entry[5]
            all_data_from_excel['simptome raportate la internare'] = entry[6]
            all_data_from_excel['diagnostic și semne de internare'] = entry[7]
            all_data_from_excel['istoric de călătorie'] = entry[8]
            all_data_from_excel['mijloace de transport folosite'] = entry[9]
            all_data_from_excel['confirmare contact cu o persoană infectată'] = entry[10]
            all_data_from_excel['data rezultat testare'] = entry[11]
            all_data_from_excel['rezultat testare'] = entry[12]
            json_data_list.append(all_data_from_excel)
        except AttributeError as e:
            print(e)
        
    print(json.dumps(json_data_list, indent=4, default=str, ensure_ascii=False))

def interact():
    fn = input("Enter a filename: ")
    return fn

def load_maze(fn):
    myfile = open(fn)
    maze_txt = myfile.read()
    myfile.close()
    return maze_txt



if __name__ == "__main__":
    
    # print("Server started.")
    # app = tornado.web.Application([
    #     (r"/", Userform),
    #     (r"/upload", Upload),
    #     (r"/blog", staticRequestHandler),
    #     (r"/isEven", querryStringRequestHandler),
    #     (r"/tweet/([0-9]+)", resourceRequestHandler),
    # ])

    # app.listen(8888)
    # print("HEY I am listening on port 8888")
    # tornado.ioloop.IOLoop.current().start()
    print(load_maze(interact()))
