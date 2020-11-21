import numpy as np
import pandas as pd
import json
from math import isnan
from constants import *
from confirmed_contact_parser import confirmed_contact_parser, check_nan
from label_parser import institution_parser, sex_parser, age_parser, result_parser
from symptom_parser import *
from parseTimeDate import parseTime
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix

class covid_detector:

    def __init__(self, config):
        with open(config, "r") as config_file:
            self.config = json.load(config_file)
        self.contact_parser = confirmed_contact_parser()
        if self.config[MODE] == TRAIN:
            self.train()
        elif self.config[MODE] == PREDICT:
            # self.model =
            pass


    def check_nan(self, e):
        return isinstance(e, float) and isnan(e)

    # Takes one sample in the dataset and performs FX
    def extract_features(self, sample):
        # Parse the source institution
        try:
            inst = institution_parser(sample[0])
        except AttributeError as e:
            print(sample[0])

        # Parse the person's sex
        s = sex_parser(sample[1])

        # Parse the age
        age = age_parser(str(sample[2]), self.mean_age)

        # Parse declared symptoms
        decl_sympt = parse_symptoms(str(sample[4]))

        # Parse the symptoms the pacient had when being admitted in the hospital
        actual_symptoms = parse_symptoms(str(sample[6]))

        # Parse the patient's contact history
        had_contact_with_infected_person = self.contact_parser.parse(str(sample[10]))

        # Parse the test results' date
        results_date = parseTime(sample[11])

        result = []
        result.append(inst)
        result.append(s)
        result.append(age)
        result.append(had_contact_with_infected_person)
        result.append(results_date)
        for i in range(len(decl_sympt)):
            result.append(decl_sympt[i])
        for i in range(len(actual_symptoms)):
            result.append(actual_symptoms[i])

        return result

    # istoric de calatorie, mijloace de transport

    def train(self):
        # Read excel
        print("Reading data", flush=True)
        df = pd.read_excel(self.config[TRAIN_PATH], na_values=None)

        # Store data in labels in separate arrays
        data = df.iloc[:, :12].values
        labels = df.iloc[:, 12].values
        
        print("Preprocessing data", flush=True)
        # Ignore mislabeled data
        X_aux = []
        y_aux = []
        n = len(data)
        for i in range(n):
            if self.check_nan(labels[i]) == False:
                if result_parser(labels[i]) != 2:
                    X_aux.append(data[i])
                    y_aux.append(result_parser(labels[i]))
        
        X = []
        y = []
        n = len(X_aux)
        # Calculate mean_age
        self.mean_age = 0
        for i in range(n):
            if self.check_nan(X_aux[i][2]) == False:
                self.mean_age += int(age_parser(str(X_aux[i][2])))
        self.mean_age = round(self.mean_age / n)
        for i in range(n):
            if self.check_nan(X_aux[i][2]):
                X_aux[i][2] = self.mean_age

        # Extract features
        print("Extracting features", flush=True)
        for i in range(n):
            X.append(self.extract_features(X_aux[i]))
            y.append(y_aux[i])

        X = np.array(X)
        y = np.array(y)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

        print("Training model", flush=True)
        self.model = RandomForestClassifier(n_estimators = 100, criterion = "entropy", max_depth = 10, random_state = 0, verbose = 1)
        # self.model.fit(X_train, y_train)
        with open("testfile.txt", "w") as outfile:
        for i in range(n):
            
        

    # Function to be used for predicting on data through the API
    def predict(self):
        pass

if __name__ == "__main__":

    detector = covid_detector("config.json")