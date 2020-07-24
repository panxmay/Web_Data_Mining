from sklearn import datasets
import random
import math
import pandas as pd

def get_dataset():
    iris = datasets.load_iris()
    names = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
    dataset = pd.DataFrame(iris.data, columns=names)
    dataset['class'] = iris.target
    return dataset

def get_max_index(data):
    max = -1
    index = -1
    for i in range(0, len(data)):
        if data[i] > max:
            index = i
            max = data[i]
    return index

def get_test_data(start, end, n):
    test_data = random.sample(range(start, end), n)
    return test_data

def compute_distance(d1, d2):
    distance = 0
    if len(d1) != len(d2):
        print("无法计算距离")
        return
    for i in range(0, len(d1)):
        distance += math.pow(d1[i] - d2[i], 2)
    return math.sqrt(distance)

def delete_test_data(dataset, n, test_data):
    test_index = get_test_data(0, 150, n)
    for i in test_index:
        test_data.append(dataset.loc[i, :])
    dataset = dataset.drop(test_index)
    dataset.reset_index(drop=True, inplace=True)
    return dataset

def KNN(k, n):
    dataset = get_dataset()
    test_data = []
    dataset = delete_test_data(dataset, n, test_data)
    for i in test_data:
        distance = []
        for index in dataset.index:
            distance.append([index, compute_distance(
                i[:4], dataset.iloc[index, 0:4])])
        distance.sort(key=lambda d: d[1], reverse=False)
        classes = [0, 0, 0]
        for j in range(0, k):
            classes[dataset.iloc[distance[j][0], 4]] += 1
        data_class = get_max_index(classes)
        print(i)
        print("预测结果：", data_class)

k = 10
n = 5
KNN(k, n)
