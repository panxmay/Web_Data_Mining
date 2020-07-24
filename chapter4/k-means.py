import pandas as pd
import random
import math
MaxSize = 100000000

# 获取数据
def get_data(filename):
    df = pd.read_csv(filename, encoding='utf-8')
    datas = []
    for index in df.index:
        datas.append((df.iloc[index, 0], df.iloc[index, 1]))
    return datas

# 初始化质心
def get_initial_centroids(datas):
    return random.choice(datas)

# 距离函数
def compute_distance(d1, d2):
    return math.pow(d1[0] - d2[0], 2) + math.pow(d1[1] - d2[1], 2)

# 算法初始化
def initial_algorithm(k):
    centroids = []
    for i in range(0, k):
        t = get_initial_centroids(datas)
        while t in centroids:
            t = get_initial_centroids(datas)
        centroids.append(t)
    return centroids

# k-means的简单版本
def k_means_simple(k, centroids):
    global flag  # 统计质心不发生变化的个数
    global cluster  # 记录聚类的结果
    global sse
    sse = 0
    cluster = []
    for i in range(0, k):
        cluster.append([])
    # 对每个数据点，聚类到最近质心的聚类
    for i in range(0, len(datas)):
        min = MaxSize
        cluster_j = 0
        for j in range(0, k):
            d = compute_distance(datas[i], centroids[j])
            if d <= min:
                min = d
                cluster_j = j
        cluster[cluster_j].append(datas[i])
    flag = 0
    bank_cluster = []
    max = 0  # 找到数量最大的聚类
    max_cluster_num = 0  # 存储最大簇的编号
    # 重新计算质心
    for i in range(0, k):
        # 如果为空类，则先跳过，暂时不处理
        if len(cluster[i]) == 0:
            bank_cluster.append(i)
            continue
        # 计算每一个新类的质心
        sum1 = 0
        sum2 = 0
        for item in cluster[i]:
            sum1 += item[0]
            sum2 += item[1]
        # 如果质心与上一次的质心相同则flag++
        if sum1 / len(cluster[i]) == centroids[i][0] and sum2 / \
                len(cluster[i]) == centroids[i][1]:
            flag += 1
        else:
            centroids[i] = (sum1 / len(cluster[i]), sum2 / len(cluster[i]))
    # 如果在本轮聚类过程中产生了空类,则首先找到包含最多数据量的聚类
    if len(bank_cluster) != 0:
        for i in range(0, k):
            if len(cluster[i]) > max:
                max = len(cluster[i])
                max_cluster_num = i
        # 找到距离最大聚类质心的数据，作为新的质心
        cluster[max_cluster_num].sort()
        # 为每一个空类，重新选择质心，并将选为实心的数据从原来的聚类删去
        for i in range(0, len(bank_cluster)):
            centroids[bank_cluster[i]] = cluster[max_cluster_num][i]
            cluster[max_cluster_num].pop(i)
    # 计算本轮sse
    for i in range(0, k):
        for data in cluster[i]:
            sse += compute_distance(centroids[i], data)
    return centroids

# k-means算法的disk版本
def k_means_disk(k, centroids):
    global flag
    global cluster
    global sse
    sse = 0
    cluster = []
    sum = []
    for i in range(0, k):
        cluster.append([])
        sum.append([0, 0])
    for i in range(0, len(datas)):
        min = MaxSize
        cluster_j = 0
        for j in range(0, k):
            d = compute_distance(datas[i], centroids[j])
            if d <= min:
                min = d
                cluster_j = j
        cluster[cluster_j].append(datas[i])
        # 在对数据进行聚类操作时，同时计算各个聚类的数据和
        sum[cluster_j][0] += datas[i][0]
        sum[cluster_j][1] += datas[i][1]
    flag = 0
    bank_cluster = []
    max = 0
    max_cluster_num = 0
    for i in range(0, k):
        # 如果为空类，则先跳过，暂时不处理
        if len(cluster[i]) == 0:
            bank_cluster.append(i)
            continue
        # 计算每一个新类的质心
        if sum[i][0] / len(cluster[i]) == centroids[i][0] and sum[i][1] / \
                len(cluster[i]) == centroids[i][1]:
            flag += 1
        else:
            centroids[i] = (sum[i][0] / len(cluster[i]),
                            sum[i][1] / len(cluster[i]))
    # 如果在本轮聚类过程中产生了空类,则首先找到包含最多数据量的聚类
    if len(bank_cluster) != 0:
        for i in range(0, k):
            if len(cluster[i]) > max:
                max = len(cluster[i])
                max_cluster_num = i
        cluster[max_cluster_num].sort()
        # 为每一个空类，重新选择质心，并将选为实心的数据从原来的聚类删去
        for i in range(0, len(bank_cluster)):
            centroids[bank_cluster[i]] = cluster[max_cluster_num][i]
            cluster[max_cluster_num].pop(i)
    # 计算本轮sse
    for i in range(0, k):
        for data in cluster[i]:
            sse += compute_distance(centroids[i], data)
    return centroids


k = 2  # 指定k值
flag = 0  # 统计质心保持不变的个数 #
cluster = []  # 存储聚类结果
sse = MaxSize
thresh_value = 0.00001  # 设定阈值
datas = get_data('data/test_k_means.csv')
cen = initial_algorithm(k)  # 得到初始质心
while True:
    sse_old = sse
    # 选择执行哪一种算法
    cen = k_means_simple(k, cen)
    cen = k_means_disk(k, cen)
    if sse_old - sse <= thresh_value or flag == k:
        break
print(cluster)
