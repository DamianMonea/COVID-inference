import string
import pandas as pd
import numpy as np
from constants import *


def isNaN(string):
    return string != string


def institution_parser(entry):
    source = entry.lower()

    if source == "x":
        return 1
    elif source == "y":
        return 2
    elif source == "z":
        return 3
    else:
        return 0


def sex_parser(entry):

    sex = entry.lower()

    if sex[0] == 'm':
        return 1
    if sex[0] == 'f':
        return 2
    else:
        return 0


def age_parser(entry, mean_age):

    age = entry.lower().replace(" ", "")

    if isNaN(age):
        return mean_age
    elif "lun" in age and "an" in age:
        return age[0]
    elif "nou" in age or "lun" in age or "zi" in age or "ore" in age:
        return 1
    elif "an" in age:
        return int("".join(filter(str.isdigit, entry)))
    elif age.isdigit():
        return age


def result_parser(entry):

    entry = entry.lower()

    if entry == "pozitiv":
        return 1
    elif entry == "negativ":
        return 0
    else:
        return 2