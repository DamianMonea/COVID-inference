import os
import json
import argparse
import sklearn
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from constants import *

def process_entry(entry):
    pass

def extract_features(entry):
    # Apel parsere pentru entry
    pass

def train(config):
    
    # Read excel
    df = pd.read_excel(config[TRAIN_PATH], na_values=None)

    # Store values in 2D array
    data = df.iloc[:].values
    processed = []
    declared_symptoms = set()
    actual_symptoms = set()
    for entry in data:
        try:
            declared = entry[4].lower()
            split_arr = declared.split(",")
            for s in split_arr:
                declared_symptoms.add(s)
        except AttributeError as e:
            pass
        try:
            actual = entry[6].lower()
            split_arr = actual.split(",")
            for s in split_arr:
                actual_symptoms.add(s)
        except AttributeError as e:
            pass
    print("Declared:", len(declared_symptoms))
    print("Actual:", len(actual_symptoms))
    pass
 
def test(config):
    pass

def main():
    config = {}
    with open("config.json", "r") as config_file:
        config = json.load(config_file)
    if config["mode"] == "train":
        train(config)
    
if __name__ == "__main__":

    main()