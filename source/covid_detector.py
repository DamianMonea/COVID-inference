import pandas as pd
from constants import *
from confirmed_contact_parser import confirmed_contact_parser, check_nan
from label_parser import institution_parser, sex_parser, age_parser, result_parser

class covid_detector:

    def __init__(self, config):
        self.config = config

    # Takes one sample in the dataset and performs FX
    def extract_features(self, sample):
        pass

    def train(self):
        # Read excel
        df = pd.read_excel(self.config[TRAIN_PATH], na_values=None)

        # Store values in 2D array
        data = df.iloc[:, :12].values
        labels = df.iloc[:, 12].values
        print(labels[:10])
        pass