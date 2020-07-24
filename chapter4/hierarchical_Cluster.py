import re
import sklearn
import pandas as pd
import random
import math


def get_data(filename):
    df = pd.read_csv(filename, encoding='utf-8')
    datas = []
    for index in df.index:
        datas.append((df.iloc[index, 0], df.iloc[index, 1]))
    return datas


def compute_distance(d1, d2):
    return math.pow(d1[0] - d2[0], 2) + math.pow(d1[1] - d2[1], 2)


def pair_wise_distance(datas, n):
    pass
