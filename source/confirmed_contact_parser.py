import json

class confirmed_contact_parser:

    def __init__(self, keyword_path = ""):
        if keyword_path == "":
            self.keywords = {"true": [], "false": []}
        else:
            with open(keyword_path, "r") as keyFile:
                self.keywords = json.load(keyFile)

    def extract_keywords(self, arr):
        for sample in arr:
            

    def parse(self, sample):
        pass

    def parse_array(self, arr):
        pass