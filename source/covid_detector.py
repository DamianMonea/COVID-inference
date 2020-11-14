class covid_detector:

    def __init__(self, config):
        self.config = config

    def train(self):
        # Read excel
        df = pd.read_excel(self.config[TRAIN_PATH], na_values=None)

        # Store values in 2D array
        data = df.iloc[:].values
        pass