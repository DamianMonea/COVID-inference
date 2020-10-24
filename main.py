import os
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sklearn

def train(path):
    pass

def test(path):
    pass

def main(args):
    if args.mode == "train":
        if args.train_path == None:
            print("Please enter the path to the training dataset.")
            exit()
        else:
            train(args.train_path)
    if args.mode == "predict":
        if args.input_file == None:
            print("Please enter the path to the test dataset.")
            exit()
        else:
            test(args.input_file)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", help="train / predict", required=True)
    parser.add_argument("--train_path", help="Path to the training dataset.")
    parser.add_argument("--input_file", help="Path to the test dataset.")
    args = parser.parse_args()
    main(args)