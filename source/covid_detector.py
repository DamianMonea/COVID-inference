import pandas as pd
import json
from math import isnan
from constants import *
from confirmed_contact_parser import confirmed_contact_parser, check_nan
from label_parser import institution_parser, sex_parser, age_parser, result_parser
from sklearn.model_selection import train_test_split

class covid_detector:

    def __init__(self, config):
        with open(config, "r") as config_file:
            self.config = json.load(config_file)

    def check_nan(self, e):
        return isinstance(e, float) and isnan(e)

    # Takes one sample in the dataset and performs FX
    def extract_features(self, sample):
        # Parse the source institution
        inst = institution_parser(sample[0])

        # Parse the person's sex
        s = sex_parser(sample[1])

        # Parse the age
        age = age_parser(sample[2], self.mean_age)

    # istoric de calatorie, mijloace de transport

    def train(self):
        # Read excel
        print(self.config[TRAIN_PATH])
        df = pd.read_excel(self.config[TRAIN_PATH], na_values=None)

        # Store data in labels in separate arrays
        data = df.iloc[:, :12].values
        labels = df.iloc[:, 12].values
        
        # Ignore mislabeled data
        X_aux = []
        y_aux = []
        n = len(data)
        for i in range(n):
            if self.check_nan(labels[i]) == False:
                if result_parser(labels[i]) != 2:
                    X_aux.append(data[i])
                    y_aux.append(result_parser(labels[i]))
        
        # Extract features
        X = []
        y = []
        n = len(X_aux)
        # Calculate mean_age
        self.mean_age = 0
        for i in range(n):
            if self.check_nan(X_aux[i][2]) == False:
                self.mean_age += int(age_parser(str(X_aux[i][2])))
        self.mean_age = int(self.mean_age / n)

        # for i in range(n):
        #     X.append(self.extract_features(X_aux[i]))
        #     y.append(y_aux[i])

    # Function to be used for predicting on data through the API
    def predict(self):
        pass

if __name__ == "__main__":

    detector = covid_detector("config.json")
    detector.train()